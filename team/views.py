from django.shortcuts import render

# Create your views here.
# 判断是否开启组队招募
# if 开启组队招募:
#     # 检查组队信息表是否存在该项目的记录
#     if 组队信息.objects.filter(项目=新项目).exists():
#         # 修改组队信息表中的数据
#         组队信息.objects.filter(项目=新项目).update(是否开启招募=True)
#     else:
#         # 插入一条新的数据到组队信息表
#         组队信息.objects.create(项目=新项目, 是否开启招募=True)

"""
在这个示例中，MembershipView继承自APIView，提供了处理队伍申请和审核的POST、PUT和DELETE方法。

对于POST方法，用户可以向队伍发出申请。我们首先检查队伍是否正在招募，然后xx检查用户是否已经是队伍的成员。如果都通过了验证，就创建一个新的Member对象，并将其保存到数据库中。

对于PUT方法，队长可以通过审核队伍成员的申请。我们首先检查队伍和队伍成员是否存在，然后检查当前用户是否是队长。如果通过了验证，就将is_approved字段设置为True，并保存到数据库中。

对于DELETE方法，队长可以删除队伍成员。我们首先检查队伍和队伍成员是否存在，然后检查当前用户是否是队长。如果通过了验证，就从数据库中删除Member对象。
"""
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from team.models import Team, Member
from team.serializers import *


# POST：提交招募信息
class TeamViewSet(ModelViewSet):
    """
    设置了 queryset 和 serializer_class 属性，分别表示操作的数据集和使用的序列化器。
    create 方法被重写，用于在创建队伍时将当前用户设置为队长。我们在 request.data 中添加了 team_leader_id 字段，将其设置为当前用户的 ID。
    list 方法被重写，用于返回队伍列表的响应。我们首先对数据集进行过滤和序列化操作，然后将序列化的数据作为响应返回。
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='队伍负责人')
    team_name = models.CharField(max_length=100, verbose_name='队伍名称')
    is_recruitment_open = models.BooleanField(verbose_name='是否开启招募', default=True)
    recruitment_requirements = models.TextField(blank=True, verbose_name='招募要求')
    recruitment_end_date = models.DateField(blank=True, null=True, verbose_name='招募结束日期')
    recruitment_slots = models.IntegerField(blank=True, null=True, verbose_name='招募人数')
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    # def create(self, request, *args, **kwargs):
    #     # request.data["team_leader_id"] = request.user  # 将队长设置为当前用户
    #     return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 处理队伍申请和审核的POST、PUT和DELETE方法
class MembershipView(APIView):
    def post(self, request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not team.is_recruitment_open:
            return Response({"message": "Team is not currently recruiting"}, status=status.HTTP_400_BAD_REQUEST)

        member = request.user
        if Member.objects.filter(team=team, user_id=member).exists():
            return Response({"message": "You are already a member of this team"}, status=status.HTTP_400_BAD_REQUEST)

        # 创建新的队伍成员
        team_member = Member(team=team, user_id=member)
        team_member.save()

        serializer = MemberSerializer(team_member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, team_id, member_id):
        try:
            team = Team.objects.get(id=team_id)
            team_member = Member.objects.get(team=team, id=member_id)
        except (Team.DoesNotExist, Member.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 只有队长有权批准队伍成员
        if team.captain != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        team_member.is_approved = True
        team_member.save()

        serializer = MemberSerializer(team_member)
        return Response(serializer.data)

    def delete(self, request, team_id, member_id):
        try:
            team = Team.objects.get(id=team_id)
            team_member = Member.objects.get(team=team, id=member_id)
        except (Team.DoesNotExist, Member.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 只有队长有权删除队伍成员
        if team.captain != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        team_member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamRecruitmentView(APIView):
    def get(self, request):
        try:
            project_id = request.data.get('project')
            team_recruitment = Team.objects.get(project=project_id)
        except Team.DoesNotExist:
            response_data = {
                'success': False,
                'message': '组队招募数据不存在',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = TeamRecruitmentSerializer(team_recruitment)
        response_data = {
            'success': True,
            'message': '组队招募数据获取成功',
            'data': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TeamRecruitmentSerializer(method='insert', data=request.data)
        if serializer.is_valid():
            # 根据当前用户创建组队招募数据
            user = request.user
            team_recruitment = serializer.save(created_by=user)

            # 执行其他逻辑或返回响应
            response_data = {
                'success': True,
                'message': '组队招募数据创建成功',
                'data': serializer.data  # 包含创建成功后的数据
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'success': False,
                'message': '组队招募数据创建失败',
                'errors': serializer.errors  # 包含序列化器错误信息
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            project_id = request.data.get('project')
            team_recruitment = Team.objects.get(project=project_id)
        except Team.DoesNotExist:
            response_data = {
                'success': False,
                'message': '组队招募数据不存在',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = TeamRecruitmentSerializer(instance=team_recruitment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'success': True,
                'message': '组队招募数据更新成功',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'success': False,
                'message': '组队招募数据更新失败',
                'errors': serializer.errors,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

class TeamApplicationView(APIView):
    def post(self, request):
        serializer = TeamApplicationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            application = serializer.save()
            response_data = {
                'success': True,
                'message': '队伍申请提交成功',
                'data': {'application_id': application.id}
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'success': False,
                'message': '队伍申请提交失败',
                'errors': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)