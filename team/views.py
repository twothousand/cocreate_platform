# 系统模块
from datetime import date
# django
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import transaction
from django.contrib.auth import get_user_model
# rest_framework
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
# common
from common.mixins import my_mixins
# app
from team import serializers as team_serializers
from team.models import Team, Member, Application
from user.permissions import IsOwnerOrReadOnly
from project.models import Project
from datetime import date

User = get_user_model()


# 组队招募
class TeamRecruitmentView(APIView):
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:  # 对于POST、PUT和DELETE请求
            permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]  # 需要用户被认证
        else:  # 对于其他请求方法，比如GET、PATCH等
            permission_classes = [AllowAny]  # 允许任何人，不需要身份验证
        return [permission() for permission in permission_classes]

    # 获得组队招募信息
    def get(self, request):
        permission_classes = [AllowAny]
        try:
            project_id = request.data.get('project')
            team_recruitment = Team.objects.get(project=project_id)
        except Team.DoesNotExist:
            response_data = {
                'message': '组队招募数据不存在',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        serializer = team_serializers.TeamRecruitmentSerializer(team_recruitment)
        response_data = {
            'message': '组队招募数据获取成功',
            'data': serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    # 创建组队招募信息
    def post(self, request):
        permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
        request.data['team_leader'] = request.user.id
        serializer = team_serializers.TeamRecruitmentSerializer(data=request.data)

        if serializer.is_valid():
            # 根据当前用户创建组队招募数据
            user = request.user
            # 校验招募截止日期是否小于今天
            recruitment_end_date = serializer.validated_data['recruitment_end_date']
            if recruitment_end_date < date.today():
                response_data = {
                    'message': '招募截止日期不能早于今天',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            team_recruitment = serializer.save(created_by=user)

            # 执行其他逻辑或返回响应
            response_data = {
                'message': '组队招募数据创建成功',
                'data': serializer.data,  # 包含创建成功后的数据
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'message': '组队招募数据创建失败',
                'data': serializer.error,  # 包含序列化器错误信息
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 更新组队招募
    def put(self, request):
        permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
        request.data['team_leader'] = request.user.id
        try:
            project_id = request.data.get('project')

            team_recruitment = Team.objects.get(project=project_id)
        except Team.DoesNotExist:
            response_data = {
                'message': '组队招募数据不存在',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        # 获取当前用户
        user = request.data.get('team_leader')

        # 判断当前用户是否是队长
        try:
            member = Member.objects.get(team=team_recruitment, user=user)
            if not member.is_leader:
                response_data = {
                    'message': '您不是队长，只有队长能更新招募',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        except Member.DoesNotExist:
            response_data = {
                'message': '您不是该团队的成员，只有队长能更新招募',
                'data': None,
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        serializer = team_serializers.TeamRecruitmentSerializer(instance=team_recruitment, data=request.data, partial=True)
        if serializer.is_valid():
            # 校验招募截止日期是否小于今天
            recruitment_end_date = serializer.validated_data['recruitment_end_date']
            if recruitment_end_date < date.today():
                response_data = {
                    'message': '招募截止日期不能早于今天',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            response_data = {
                'message': '组队招募数据更新成功',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'message': '组队招募数据更新失败',
                'data': serializer.errors,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


# 组队申请：提交组队申请（可多次，覆盖）
class TeamApplicationView(my_mixins.LoggerMixin, my_mixins.CreatRetrieveUpdateModelViewSet):
    queryset = Application.objects.all()
    serializer_class = team_serializers.TeamApplicationSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:  # 对于POST、PUT和DELETE请求
            permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]  # 需要用户被认证
        else:  # 对于其他请求方法，比如GET、PATCH等
            permission_classes = [AllowAny]  # 允许任何人，不需要身份验证
        return [permission() for permission in permission_classes]

    @transaction.atomic
    @action(methods=['POST'], detail=True)
    def create_application(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            project_id = request.data.get('project_id')
            team_id = request.data.get('team_id')
            application_msg = request.data.get('application_msg')

            if not user_id or not team_id:
                response_data = {
                    'message': '请提供用户ID(token), 队伍ID(team_id), application_msg, 申请消息(application_msg)',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            user_instance = get_object_or_404(User, id=user_id)
            team_instance = get_object_or_404(Team, id=team_id)
            project_instance = get_object_or_404(Project, id=project_id)
            # 检查用户是否已经在队伍中且状态正常
            existing_user = Member.objects.filter(
                Q(team=team_id) &
                Q(user=user_id) &
                Q(member_status='正常')
            ).first()

            print('existing_user',existing_user)
            if existing_user:
                response_data = {
                    'message': '用户已经在队伍中，无需继续申请。',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # 检查申请是否已经存在
            existing_application = Application.objects.filter(
                Q(user=user_id) &
                Q(project=project_id) &
                Q(team=team_id)
            ).first()

            if existing_application and existing_application.status=='待审核':
                # # 如果申请已经存在，更新其内容 先注释掉这个逻辑
                # existing_application.application_msg = application_msg
                # existing_application.status = '待审核'
                # existing_application.save()
                # application = existing_application

                response_data = {
                    'message': '申请在审核中，无需继续申请。',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            elif existing_application and existing_application.status != '待审核':
                # 如果申请已经存在，更新其内容
                existing_application.application_msg = application_msg
                existing_application.status = '待审核'
                existing_application.save()
                serializer = self.get_serializer(existing_application)
                response_data = {
                    'message': '重新发送申请',
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                # 如果没有申请存在，创建新的申请
                application = Application.objects.create(
                    team=team_instance,
                    user=user_instance,
                    application_msg=application_msg,
                    project=project_instance,
                )
                serializer = self.get_serializer(application)
                response_data = {
                    'message': '队伍申请提交成功',
                    'data': serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # 显式地触发回滚操作
            transaction.set_rollback(True)
            response_data = {
                'message': '队伍申请提交失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


    # 接口：处理组队申请（PUT）
    @transaction.atomic
    @action(methods=['PUT'], detail=True)
    def application_update(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            application_id = request.data.get('application_id')
            application_status = request.data.get('decision')
            if not application_id or not application_status or not user_id:
                response_data = {
                    'message': '请提供当前处理用户ID(token), 申请ID(application_id), 处理意见(decision)[同意加入、拒绝]',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            application_instance = get_object_or_404(Application, id=application_id)
            # 获取对应的Team实例
            team_instance = get_object_or_404(Team, id=application_instance.team_id)
            # 获取对应的User实例
            user_instance = get_object_or_404(User, id=user_id)
            # 检查当前用户是否是队长
            is_leader = Member.objects.filter(team=team_instance, user=user_instance, is_leader=True).exists()
            if not is_leader:
                response_data = {
                    'message': '只有队长才有权限处理组队申请',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)

            # 如果不是待审核状态则返回
            if application_instance.status != '待审核':
                response_data = {
                    'message': '当前申请不是待审核状态',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            # 获取申请表中的User实例
            application_user_instance = get_object_or_404(User, id=application_instance.user_id)
            if application_status == '同意加入':
                # 更改申请状态为同意加入
                application_instance.status = '同意加入'
                application_instance.save()

                # 检查用户是否已经是队伍成员且状态正常
                existing_member = Member.objects.filter(
                    team=team_instance,
                    user=application_user_instance,
                    member_status='正常'
                ).first()
                if existing_member:
                    response_data = {
                        'message': '该用户已经是队伍成员。',
                        'data': None,
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

                #  检查用户是否已经是队伍成员非状态正常
                leave_member = Member.objects.filter(
                    Q(team=team_instance) &
                    Q(user=application_user_instance) &
                    (Q(member_status='已离开') | Q(member_status='被移除'))
                ).first()

                if leave_member:
                    leave_member.member_status = '正常'
                    leave_member.save()
                    response_data = {
                        'message': '已重新添加该用户',
                        'data': None,
                    }
                    return Response(response_data, status=status.HTTP_200_OK)

                # 在成员表中插入一条数据
                Member.objects.create(
                    team=team_instance,
                    user=application_user_instance,
                    is_leader=0,
                    join_date=date.today(),
                    member_status='正常'
                )

                response_data = {
                    'message': '队伍申请已同意',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            elif application_status == '拒绝':
                # 更改申请状态为拒绝
                application_instance.status = '拒绝'
                application_instance.save()

                response_data = {
                    'message': '队伍申请已拒绝',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            else:
                response_data = {
                    'message': '无效的状态，decision有效值为待审核、拒绝、同意加入',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # 显式地触发回滚操作
            transaction.set_rollback(True)
            response_data = {
                'message': '处理队伍申请失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def get_pending_applications(self, request, *args, **kwargs):
        permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
        try:
            user_id = request.user.id
            team_id = request.data.get('team_id', None)

            if not user_id or not team_id:
                response_data = {
                    'message': '请提供用户ID(token)和队伍ID(team_id)。',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            try:
                team = Team.objects.get(id=team_id)
                # # 未开启组队招募情况下，屏蔽组队申请消息
                # if not team.is_recruitment_open:
                #     response_data = {
                #         'code': 200,
                #         'message': '未开启组队招募。',
                #         'data': None,
                #     }
                #     return Response(response_data, status=status.HTTP_200_OK)

                member = Member.objects.filter(team=team_id, user=user_id, is_leader=True).first()

                if not member:
                    response_data = {
                        'message': '您不是队长，无法查询组队申请信息。',
                        'data': None,
                    }
                    return Response(response_data, status=status.HTTP_403_FORBIDDEN)

                # 查询待审核的组队申请
                pending_applications = Application.objects.filter(
                    team=team_id,
                    status='待审核'
                )

                serializer = team_serializers.TeamApplicationSerializer(pending_applications, many=True)

                response_data = {
                    'message': '查询成功',
                    'data': serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            except Team.DoesNotExist:
                response_data = {
                    'message': '未找到对应的队伍',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                response_data = {
                    'message': '服务器错误',
                    'data': {'error': str(e)},
                }
                return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            response_data = {
                'message': '查询队伍申提交失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# 队伍管理
class TeamMemberViewSet(my_mixins.LoggerMixin, my_mixins.CreatRetrieveUpdateModelViewSet):
    serializer_class = team_serializers.MemberSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:  # 对于POST、PUT和DELETE请求
            permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]  # 需要用户被认证
        else:  # 对于其他请求方法，比如GET、PATCH等
            permission_classes = [AllowAny]  # 允许任何人，不需要身份验证
        return [permission() for permission in permission_classes]

    def determine_action(self, request):
        if request.method == 'GET':
            self.action = 'retrieve'
        elif request.method == 'POST':
            self.action = 'create'
        elif request.method == 'PUT':
            self.action = 'partial_update'
        else:
            self.action = None

    # 接口1：转让队长（PUT）
    @transaction.atomic
    @action(methods=['PUT'], detail=True)
    def transfer_leadership(self, request, *args, **kwargs):
        try:
            team_id = request.data.get('team_id')
            new_leader_id = request.data.get('new_leader_id')
            user_id = request.user.id
            if not team_id or not new_leader_id or not user_id:
                response_data = {
                    'message': '请提供操作用户ID(token),队伍ID(team_id),新队长用户ID(new_leader_id）',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            team_instance = get_object_or_404(Team, id=team_id)
            new_leader_instance = get_object_or_404(User, id=new_leader_id)
            current_user_instance = get_object_or_404(User, id=user_id)  # 获取当前用户

            # 检查当前用户是否是队长
            is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
            if not is_leader:
                response_data = {
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
                'message': '队长转让成功',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            # 显式地触发回滚操作
            transaction.set_rollback(True)
            response_data = {
                'message': '队长转让失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 接口2：移除队员（PUT）
    @transaction.atomic
    @action(methods=['PUT'], detail=True)
    def remove_member(self, request, *args, **kwargs):
        try:
            team_id = request.data.get('team_id')
            member_id = request.data.get('member_id')
            user_id = request.user.id  # 当前用户的ID
            if not team_id or not member_id or not user_id:
                response_data = {
                    'message': '请提供操作用户ID(token),队伍ID(team_id),队员用户ID(member_id）',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            team_instance = get_object_or_404(Team, id=team_id)
            current_user_instance = get_object_or_404(User, id=user_id)  # 获取当前用户
            member_instance = get_object_or_404(User, id=member_id)  # 获取被操作用户

            # 检查当前用户是否是队长
            is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
            if not is_leader:
                response_data = {
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
                'message': '队员移除成功',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            # 显式地触发回滚操作
            transaction.set_rollback(True)
            response_data = {
                'message': '队员移除失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 接口3：自动退出（PUT）
    @transaction.atomic
    @action(methods=['PUT'], detail=True)
    def auto_exit(self, request, *args, **kwargs):
        try:
            team_id = request.data.get('team_id')
            user_id = request.user.id

            if not team_id or not user_id:
                response_data = {
                    'message': '请提供操作用户ID(user_id),队伍ID(team_id)',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

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
                    'message': '您不是有效的队伍成员。',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # 检查当前用户是否是队长, 如果是队长，先转让队长，才能退出
            is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
            if is_leader:
                response_data = {
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
                'message': '队员已退出队伍',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            # 显式地触发回滚操作
            transaction.set_rollback(True)
            response_data = {
                'message': '退出队伍失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # 接口4：添加队员（POST）
    @transaction.atomic
    @action(methods=['POST'], detail=True)
    def add_member(self, request, *args, **kwargs):
        try:
            team_id = request.data.get('team_id')
            user_id = request.user.id
            member_id = request.data.get('member_id')
            if not team_id or not user_id:
                response_data = {
                    'message': '请提供操作用户ID(token),队伍ID(team_id),成员用户ID(member_id)',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            team_instance = get_object_or_404(Team, id=team_id)
            current_user_instance = get_object_or_404(User, id=user_id)  # 获取当前用户
            member_instance = get_object_or_404(User, id=member_id)

            # 检查当前用户是否是队长
            is_leader = Member.objects.filter(team=team_instance, user=current_user_instance, is_leader=True).exists()
            if not is_leader:
                response_data = {
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
                serializer = self.get_serializer(existing_member)
                response_data = {
                    'message': '该用户已经是队伍成员。',
                    'data': serializer.data,
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
                serializer = self.get_serializer(leave_member)
                response_data = {
                    'message': '已重新添加该用户',
                    'data': serializer.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)

            # 将用户添加为队伍的新成员
            new_member = Member.objects.create(
                team=team_instance,
                user=member_instance,
                is_leader=0,
                join_date=date.today(),
                member_status='正常'
            )
            serializer = self.get_serializer(new_member)

            response_data = {
                'message': '成功添加该用户',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # 显式地触发回滚操作
            transaction.set_rollback(True)
            response_data = {
                'message': '添加用户失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True)
    def get_all_members(self, request, *args, **kwargs):
        try:
            team_id = request.data.get('team_id')
            if not team_id:
                response_data = {
                    'message': '请提供队伍ID(team_id)。',
                    'data': None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            team_instance = get_object_or_404(Team, id=team_id)

            # Get all members of the team
            all_members = Member.objects.filter(team=team_instance, member_status='正常')

            # Serialize the member data and return the response
            serializer = self.get_serializer(all_members, many=True)
            response_data = {
                'message': '查询队伍所有成员信息成功',
                'data': serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': '查询队伍所有成员信息失败',
                'data': {'errors': str(e)}
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)