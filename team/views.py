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



# 组队招募
class TeamRecruitmentView(APIView):
    # 获得组队招募信息
    def get(self, request):
        try:
            project_id = request.data.get('project')
            team_recruitment = Team.objects.get(project=project_id)
        except Team.DoesNotExist:
            response_data = {
                'code': 404,
                'message': '组队招募数据不存在',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = TeamRecruitmentSerializer(team_recruitment)
        response_data = {
            'code': 200,
            'message': '组队招募数据获取成功',
            'data': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    # 创建组队招募信息
    def post(self, request):
        serializer = TeamRecruitmentSerializer(method='insert', data=request.data)
        if serializer.is_valid():
            # 根据当前用户创建组队招募数据
            user = request.user
            team_recruitment = serializer.save(created_by=user)

            # 执行其他逻辑或返回响应
            response_data = {
                'code': 201,
                'message': '组队招募数据创建成功',
                'data': serializer.data,  # 包含创建成功后的数据
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'code': 400,
                'message': '组队招募数据创建失败',
                'data': serializer.errors,  # 包含序列化器错误信息
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 更新组队招募
    def put(self, request):
        try:
            project_id = request.data.get('project')
            team_recruitment = Team.objects.get(project=project_id)
        except Team.DoesNotExist:
            response_data = {
                'code': 404,
                'message': '组队招募数据不存在',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = TeamRecruitmentSerializer(instance=team_recruitment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'code': 200,
                'message': '组队招募数据更新成功',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'code': 400,
                'message': '组队招募数据更新失败',
                'data': serializer.errors,
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
            project_id = serializer.validated_data['project']
            team_id = serializer.validated_data['team']

            # 检查用户是否已经在队伍中且状态正常
            existing_user = Member.objects.filter(
                Q(team=team_id) &
                Q(user=user_id) &
                Q(member_status='正常')
            ).first()

            if existing_user:
                response_data = {
                    'code': 400,
                    'message': '您已经在队伍中，无需继续申请。',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # 检查申请是否已经存在
            existing_application = Application.objects.filter(
                Q(user=user_id) &
                Q(project=project_id) &
                Q(team=team_id)
            ).first()

            if existing_application:
                # 如果申请已经存在，更新其内容
                existing_application.application_msg = serializer.validated_data['application_msg']
                existing_application.status = '待审核'
                # 添加其他需要更新的字段

                existing_application.save()
                application = existing_application
            else:
                # 如果没有申请存在，创建新的申请
                application = serializer.save()

        except Exception as e:
            response_data = {
                'code': 400,
                'message': '队伍申请提交失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            'code': 201,
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
                'code': 200,
                'message': '队伍申请已同意',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        elif status == '拒绝':
            # 更改申请状态为拒绝
            application_instance.status = '拒绝'
            application_instance.save()

            response_data = {
                'code': 200,
                'message': '队伍申请已拒绝',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            response_data = {
                'code': 400,
                'message': '无效的状态',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


# 队伍管理
class TeamMemberViewSet(ModelViewSet):
    serializer_class = MemberSerializer

    # 接口1：转让队长（PUT）
    @action(methods=['PUT'], detail=True)
    def transfer_leadership(self, request, *args, **kwargs):
        team_id = request.data.get('team_id')
        new_leader_id = request.data.get('new_leader_id')
        user_id = request.data.get('user_id')  # 当前用户的ID

        team_instance = get_object_or_404(Team, id=team_id)
        new_leader_instance = get_object_or_404(User, id=new_leader_id)
        current_user_instance = get_object_or_404(User, id=user_id)  # 获取当前用户

        # 检查当前用户是否是队长
        is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
        if not is_leader:
            response_data = {
                'code': 403,
                'message': '只有队长才有权限进行转让。',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        # 检查新队长是否已经是队伍成员且状态正常
        existing_member = Member.objects.filter(
            team=team_instance,
            user=new_leader_instance,
            member_status='正常'
        ).first()

        if not existing_member:
            response_data = {
                'code': 400,
                'message': '指定的新队长不是有效的队伍成员。',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # 更新原队长的is_leader字段为False，新队长的is_leader字段为True
        current_user_member = Member.objects.get(team=team_instance, user=current_user_instance)
        current_user_member.is_leader = False
        current_user_member.save()

        existing_member.is_leader = True
        existing_member.save()

        # 序列化并返回数据
        serializer = self.get_serializer(existing_member)
        response_data = {
            'code': 200,
            'message': '队长转让成功',
            'data': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

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
        if not is_leader:
            response_data = {
                'code': 403,
                'message': '只有队长才有权限移除队员。',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        # 检查队员是否是有效的队伍成员
        existing_member = Member.objects.filter(
            team=team_instance,
            user=member_instance,
            member_status='正常'
        ).first()

        if not existing_member:
            response_data = {
                'code': 400,
                'message': '指定的队员不是有效的队伍成员。',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # 将队员状态设为'被移除'
        existing_member.member_status = '被移除'
        existing_member.leave_date = date.today()
        existing_member.save()

        # 序列化并返回数据
        serializer = self.get_serializer(existing_member)
        response_data = {
            'code': 200,
            'message': '队员移除成功',
            'data': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


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
                'code': 400,
                'message': '您不是有效的队伍成员。',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # 检查当前用户是否是队长, 如果是队长，先转让队长，才能退出
        is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
        if is_leader:
            response_data = {
                'code': 403,
                'message': '队长需先转让队长身份，才能退出团队',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        # 将用户状态设为'已离开'
        existing_member.member_status = '已离开'
        existing_member.leave_date = date.today()
        existing_member.save()

        # 序列化并返回数据
        serializer = self.get_serializer(existing_member)
        response_data = {
            'code': 200,
            'message': '队员已退出队伍',
            'data': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

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
        if not is_leader:
            response_data = {
                'code': 403,
                'message': '只有队长才有权限添加队员。',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        # 检查被添加用户是否已经是队伍成员且状态正常
        existing_member = Member.objects.filter(
            team=team_instance,
            user=member_instance,
            member_status='正常'
        ).first()

        if existing_member:
            response_data = {
                'code': 400,
                'message': '该用户已经是队伍成员。',
                'data': None,
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
                'code': 200,
                'message': '已重新添加该用户',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        # 将用户添加为队伍的新成员
        Member.objects.create(
            team=team_instance,
            user=member_instance,
            is_leader=0,
            join_date=date.today(),
            member_status='正常'
        )

        response_data = {
            'code': 201,
            'message': '已添加该用户',
            'data': None,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
