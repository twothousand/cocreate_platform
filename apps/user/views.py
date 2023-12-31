# 系统模块
from datetime import datetime

# django模块
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q

# rest_framework模块
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView

# app
from apps.product.models import Product
from apps.product.serializers import VersionDetailSerializer, ProductSerializer, VersionSerializer
from apps.project.models import Project
from apps.project.serializers import UserManagedProjectsSerializer, UserManagedProjectDetailSerializer, \
    UserJoinedProjectsSerializer, UserJoinedProjectDetailSerializer
from apps.team.models import Member
from apps.user import serializers
from apps.user.permissions import IsOwnerOrReadOnly

# common
from common.mixins import my_mixins

User = get_user_model()


# 登录
class LoginView(my_mixins.LoggerMixin, my_mixins.CustomResponseMixin, TokenObtainPairView):
    serializer_class = serializers.UserLoginSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # self.log_request(self, logger, request)

        # 自定义响应message
        self.custom_message = "登录成功！"

        # 执行父类方法
        response = super().post(request, *args, **kwargs)

        # self.log_response(self, logger, request, response)
        return response


# 用于列出或检索用户的视图集
class UserViewSet(my_mixins.CustomResponseMixin, my_mixins.CreatRetrieveUpdateModelViewSet):
    queryset = User.objects.all()

    # serializer_class = UserSerializer  # 优先使用 get_serializer_class 返回的序列化器
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        重写get_permissions，实例化并返回此视图需要的权限列表。
        @return: # 返回相应的权限列表
        """
        if self.action in ['create', 'get_detail', 'reset_password']:  # 如果操作是 'create' （对应POST请求，即注册）或 'detail'
            permission_classes = [AllowAny]  # 允许任何人，不需要身份验证
        else:  # 其他操作
            permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]  # 需要用户被认证
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['create']:
            return serializers.UserRegSerializer
        elif self.action in ['partial_update', 'reset_password']:
            return serializers.UserPwdChangeSerializer
        elif self.action == "get_detail":
            return serializers.UserReadOnlySerializer
        else:
            return serializers.UserSerializer

    def retrieve(self, request, *args, **kwargs):
        self.custom_message = "用户信息获取成功"
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.custom_message = "用户注册成功"
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if self.action == "partial_update":
            self.custom_message = "用户密码修改成功"
        elif self.action == "update":
            self.custom_message = "用户信息修改成功"
        return super().update(request, *args, **kwargs)

    @action(methods=["GET"], detail=True)
    def get_detail(self, request, *args, **kwargs):
        self.custom_message = "用户信息获取成功"
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        # 首先，用你的序列化器验证提交的数据
        serializer = serializers.UserPwdChangeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # 数据验证成功后，根据手机号查找用户
        user = User.objects.get(username=serializer.validated_data["username"])

        # 使用serializer的update方法更新密码
        serializer.update(user, serializer.validated_data)

        self.custom_message = "密码重置成功"
        return Response(status=200)

    # @disallow_methods(['DELETE'])
    # @disallow_actions(['list'])
    # @transaction.atomic
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    # def perform_destroy(self, instance):
    #     """
    #     重写删除方法，改为逻辑删除
    #     @param instance:
    #     @return:
    #     """
    #     instance.is_deleted = True
    #     # TODO: 关联项目需要特殊处理
    #     instance.save()


# ------------------------我管理的项目-------------------------
# 获取特定用户管理的所有项目
class UserManagedProjectsView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    def get(self, request):
        try:
            user_id = request.user.id
            # 从Member表里获取用户管理的项目，再从Project表里获取项目信息(项目创建者不变，转移队长后，更新在Member表里的is_leader字段)
            managed_projects = Project.objects.filter(  # filter方法可以返回多个对象
                Q(team__member__user_id=user_id) & Q(team__member__is_leader=True))
            serializer = UserManagedProjectsSerializer(managed_projects, many=True)
            response_data = {
                'message': '已成功检索到用户管理的项目！',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': '检索用户管理的项目失败！！！',
                'data': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 特定用户管理的特定项目的详细信息（获取、更新、删除）
class UserManagedProjectDetailView(APIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

    @staticmethod
    def get_managed_project(user_id, project_id):
        # 从Member表里获取用户管理的项目，再从Project表里获取项目信息(项目创建者不变，转移队长后，更新在Member表里的is_leader字段)
        project = Project.objects.get(  # get方法只能返回一个对象
            Q(id=project_id) & Q(team__member__user_id=user_id) & Q(team__member__is_leader=True))
        if not project:
            raise NotFound("项目未发现或不是项目管理者！")
        return project

    def get(self, request, project_id):
        try:
            user_id = request.user.id
            project = self.get_managed_project(user_id, project_id)
            serializer = UserManagedProjectDetailSerializer(project)
            response_data = {
                "message": "获取项目信息成功！",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except NotFound as e:
            response_data = {
                "message": str(e),
                "data": None
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, project_id):
        try:
            user_id = request.user.id
            project = self.get_managed_project(user_id, project_id)
            serializer = UserManagedProjectsSerializer(project, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response_data = {
                "message": "更新项目信息成功！",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except NotFound as e:
            response_data = {
                "message": str(e),
                "data": None
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "message": "更新项目信息失败！！！",
                "data": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, project_id):
        try:
            user_id = request.user.id
            project = self.get_managed_project(user_id, project_id)
            project.delete()
            response_data = {
                "message": "项目删除成功！",
                "data": None
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except NotFound as e:
            response_data = {
                "message": str(e),
                "data": None
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {
                "message": "项目删除失败！！！",
                "data": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------------我发布的项目产品-------------------------
# 特定用户管理的特定产品的详细信息（获取、更新）
class UserPublishedProductDetailView(APIView):
    @staticmethod
    def get_managed_product(user_id, project_id):
        project = Project.objects.filter(id=project_id, project_creator_id=user_id).first()
        if not project:
            raise NotFound("项目未发现或不是项目管理者！")
        return project

    def get(self, request, project_id):
        try:
            user_id = request.user.id
            product = Product.objects.get(project_id=project_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Exception as e:
            response_data = {
                'message': str(e),
                'data': None
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, project_id):
        try:
            user_id = request.user.id
            serializer = VersionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                'message': str(e),
                'data': None
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, project_id):
        try:
            user_id = request.user.id
            serializer = VersionDetailSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            response_data = {
                'message': str(e),
                'data': None
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------------我加入的项目-------------------------
# 获取特定用户加入的所有项目
class UserJoinedProjectsView(APIView):
    def get(self, request):
        try:
            user_id = request.user.id

            # 获取符合条件的队伍ID列表
            team_ids = Member.objects.filter(
                user_id=user_id,
                is_leader=0,
                member_status="正常"
            ).values('team_id').distinct()
            # 如果队伍ID列表为空，则返回错误信息
            if not team_ids.exists():
                response_data = {
                    'message': '用户未加入任何项目！',
                    'data': None
                }
                return Response(response_data, status=status.HTTP_200_OK)
            # 查询与这些队伍关联的项目
            joined_projects = Project.objects.filter(team__id__in=team_ids)  # 通过team__id__in来筛选与给定队伍ID列表相关联的项目

            # 使用序列化器来序列化数据
            serializer = UserJoinedProjectsSerializer(joined_projects, many=True)
            response_data = {
                'message': '已成功检索到用户加入的项目！',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': '检索用户加入的项目失败！！！',
                'data': str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 特定用户参与的特定项目的详细信息（获取、退出）
class UserJoinedProjectDetailView(APIView):
    # 根据user_id和project_id获取相应的项目
    def get_project(self, user_id, project_id):
        try:
            project = Project.objects.get(id=project_id)
            team_member = Member.objects.get(team__project=project, user_id=user_id)
            if team_member.is_leader:
                raise PermissionDenied("你是项目管理者！！！")
            return project
        except (Project.DoesNotExist, Member.DoesNotExist):
            raise NotFound("你还未加入该项目！！！")

    def get(self, request, project_id):
        try:
            user_id = request.user.id
            project = self.get_project(user_id, project_id)
            serializer = UserJoinedProjectDetailSerializer(project)
            response_data = {
                "message": "获取加入的具体项目成功！",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "message": "获取加入的具体项目失败！！！",
                "data": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, project_id):
        try:
            user_id = request.user.id
            project = self.get_project(user_id, project_id)

            # 判断用户是否为项目负责人
            member = Member.objects.get(user_id=user_id, team__project=project_id)
            if member.is_leader:
                response_data = {
                    "message": "项目负责人无法退出项目！",
                    "data": None
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # 更新Member表中的member_status为"已离开"，leave_date为当前日期
            member.member_status = "已离开"
            member.leave_date = datetime.now()
            member.save()

            serializer = UserJoinedProjectsSerializer(project)
            response_data = {
                "message": "退出加入的项目成功！",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Member.DoesNotExist:
            response_data = {
                "message": "用户未加入该项目！",
                "data": None
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            response_data = {
                "message": "退出加入的项目失败！",
                "data": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 用户搜索
class UserSearchView(APIView):
    def get(self, request, *args, **kwargs):
        permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
        try:
            keyword = self.request.GET.get('keyword')

            if keyword == '' or keyword is None:
                response_data = {
                    "message": "无检索关键词",
                    "data": None
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            queryset = User.objects.all()

            # 应用搜索条件
            if keyword:
                queryset = queryset.filter(
                    Q(username=keyword) |
                    Q(nickname__icontains=keyword)
                )

            queryset = queryset.order_by('-nickname')
            serializer = serializers.UserSearchSerializer(queryset, many=True)

            if serializer.data:
                response_data = {
                    'message': '已成功检索到用户！',
                    'data': serializer.data
                }
            else:
                response_data = {
                    'message': '未检索到任何符合的用户！',
                    'data': serializer.data
                }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': str(e),
                'data': []
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
