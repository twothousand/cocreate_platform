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
from rest_framework.decorators import action
from team.models import Team, Member
from user.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from team.serializers import *
from datetime import date

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

#组队招募
class TeamRecruitmentView(APIView):
    #获得组队招募信息
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

    #创建组队招募信息
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
    #更新组队招募
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

# 组队申请：提交组队申请（可多次，覆盖）
class TeamApplicationView(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = TeamApplicationSerializer
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_id = serializer.validated_data['user']
            print('serializer.validated_data',serializer.validated_data)
            print('user_id',user_id)
            project_id = serializer.validated_data['project']
            team_id = serializer.validated_data['team']

            # Check if the user is already in the team and their status is normal
            existing_user = Member.objects.filter(
                Q(team=team_id) &
                Q(user=user_id) &
                Q(member_status='正常')
            ).first()

            if existing_user:
                response_data = {
                    'success': False,
                    'message': '您已经在队伍中，无需继续申请。',
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Check if the application already exists
            existing_application = Application.objects.filter(
                Q(user=user_id) &
                Q(project=project_id) &
                Q(team=team_id)
            ).first()

            if existing_application:
                # If an application already exists, update its content
                existing_application.application_msg = serializer.validated_data['application_msg']
                existing_application.status = '待审核'
                # Add other fields that need to be updated

                existing_application.save()
                application = existing_application
            else:
                # If no application exists, create a new one
                application = serializer.save()

        except Exception as e:
            response_data = {
                'success': False,
                'message': '队伍申请提交失败',
                'errors': str(e)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            'success': True,
            'message': '队伍申请提交成功',
            'data': {'application_id': application.id}
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        application_id = kwargs['id']
        application_instance = get_object_or_404(Application, id=application_id)
        status = request.data.get('status')
        if status == '同意加入':
            # 更改申请状态为同意加入
            application_instance.status = '同意加入'
            application_instance.save()
            # 获取对应的Team实例
            team_instance = Team.objects.get(id=application_instance.team_id)
            # 获取对应的User实例
            user_instance = get_object_or_404(User, id=application_instance.user_id)
            # 在成员表中插入一条数据
            Member.objects.create(
                team=team_instance,
                user=user_instance,
                is_leader=0,
                join_date=date.today(),
                member_status='正常'
            )

            response_data = {
                'success': True,
                'message': '队伍申请已同意',
            }
            return Response(response_data, status=200)

        elif status == '拒绝':
            # 更改申请状态为拒绝
            application_instance.status = '拒绝'
            application_instance.save()

            response_data = {
                'success': True,
                'message': '队伍申请已拒绝',
            }
            return Response(response_data, status=200)

        else:
            response_data = {
                'success': False,
                'message': '无效的状态',
            }
            return Response(response_data, status=400)


## 队伍管理
class TeamMemberViewSet(ModelViewSet):
    serializer_class = MemberSerializer

    # 接口1：转让队长（PUT）
    @action(methods=['PUT'], detail=True)
    def transfer_leadership(self, request, *args, **kwargs):
        print('转让队长（PUT） request.data',request.data)
        team_id = request.data.get('team_id')
        new_leader_id = request.data.get('new_leader_id')
        user_id = request.data.get('user_id')  # 当前用户的ID

        team_instance = get_object_or_404(Team, id=team_id)
        new_leader_instance = get_object_or_404(User, id=new_leader_id)
        current_user_instance = get_object_or_404(User, id=user_id)  # 获取当前用户


        # 检查当前用户是否是队长
        is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
        print('is_leader', is_leader)
        if not is_leader:
            response_data = {
                'success': False,
                'message': '只有队长才有权限进行转让。',
            }
            return Response(response_data, status=403)

        # 检查新队长是否已经是队伍成员且状态正常
        existing_member = Member.objects.filter(
            team=team_instance,
            user=new_leader_instance,
            member_status='正常'
        ).first()

        if not existing_member:
            response_data = {
                'success': False,
                'message': '指定的新队长不是有效的队伍成员。',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # 更新原队长的is_leader字段为False，新队长的is_leader字段为True
        current_user_member = Member.objects.get(team=team_instance, user=current_user_instance)
        print('current_user_member',current_user_member)
        current_user_member.is_leader = False
        current_user_member.save()

        existing_member.is_leader = True
        print('existing_member', current_user_member)
        existing_member.save()

        # 序列化并返回数据
        serializer = self.get_serializer(existing_member)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 接口2：移除队员（PUT）
    @action(methods=['PUT'], detail=True)
    def remove_member(self, request, *args, **kwargs):
        team_id = request.data.get('team_id')
        member_id = request.data.get('member_id')
        user_id = request.data.get('user_id')  # 当前用户的ID
        team_instance = get_object_or_404(Team, id=team_id)
        current_user_instance = get_object_or_404(User, id=user_id)  # 获取当前用户
        member_instance = get_object_or_404(User, id=member_id)  # 获取被操作用户

        # 检查当前用户是否是队长
        is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
        print('is_leader', is_leader)
        if not is_leader:
            response_data = {
                'success': False,
                'message': '只有队长才有权限移除队员。',
            }
            return Response(response_data, status=403)

        # 检查队员是否是有效的队伍成员
        existing_member = Member.objects.filter(
            team=team_instance,
            user=member_instance,
            member_status='正常'
        ).first()

        if not existing_member:
            response_data = {
                'success': False,
                'message': '指定的队员不是有效的队伍成员。',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # 将队员状态设为'被移除'
        existing_member.member_status = '被移除'
        existing_member.leave_date = date.today()
        existing_member.save()

        # 序列化并返回数据
        serializer = self.get_serializer(existing_member)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 接口3：自动退出（PUT）
    @action(methods=['PUT'], detail=True)
    def auto_exit(self, request, *args, **kwargs):
        team_id = request.data.get('team_id')
        user_id = request.data.get('user_id')
        team_instance = get_object_or_404(Team, id=team_id)
        current_user_instance = get_object_or_404(User, id=user_id)  # 获取当前用户

        # 检查用户是否是有效的队伍成员
        existing_member = Member.objects.filter(
            team=team_instance,
            user=current_user_instance,
            member_status='正常'
        ).first()

        if not existing_member:
            response_data = {
                'success': False,
                'message': '您不是有效的队伍成员。',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # 检查当前用户是否是队长, 如果是队长，先转让队长，才能退出
        is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
        if is_leader:
            response_data = {
                'success': False,
                'message': '队长需先转让队长身份，才能退出团队',
            }
            return Response(response_data, status=403)

        # 将用户状态设为'已离开'
        existing_member.member_status = '已离开'
        existing_member.leave_date = date.today()
        existing_member.save()

        # 序列化并返回数据
        serializer = self.get_serializer(existing_member)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 接口4：添加队员（POST）
    @action(methods=['POST'], detail=True)
    def add_member(self, request, *args, **kwargs):
        team_id = request.data.get('team_id')
        user_id = request.data.get('user_id')
        member_id = request.data.get('member_id')
        team_instance = get_object_or_404(Team, id=team_id)
        current_user_instance = get_object_or_404(User, id=user_id)  # 获取当前用户
        member_instance = get_object_or_404(User, id=member_id)

        # 检查当前用户是否是队长
        is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
        print('is_leader', is_leader)
        if not is_leader:
            response_data = {
                'success': False,
                'message': '只有队长才有权限添加队员。',
            }
            return Response(response_data, status=403)

        # 检查被添加用户是否已经是队伍成员且状态正常
        existing_member = Member.objects.filter(
            team=team_instance,
            user=member_instance,
            member_status='正常'
        ).first()

        if existing_member:
            response_data = {
                'success': False,
                'message': '该用户已经是队伍成员。',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        #  检查用户是否已经是队伍成员非状态正常
        leave_member = Member.objects.filter(
            Q(team=team_instance) &
            Q(user=member_instance) &
            (Q(member_status='已离开') | Q(member_status='被移除'))
        ).first()

        if leave_member:
            leave_member.member_status = '正常'
            leave_member.save()
            response_data = {
                'success': True,
                'message': '已重新添加该用户',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # 将用户添加为队伍的新成员
        Member.objects.create(
            team=team_instance,
            user=member_instance,
            is_leader=0,
            join_date=date.today(),
            member_status='正常'
        )

        response_data = {
            'success': True,
            'message': '已添加该用户',
        }
        return Response(response_data, status=status.HTTP_201_CREATED)