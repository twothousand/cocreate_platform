# django模块
from django.contrib.auth import get_user_model

# rest_framework模块
from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

# app
from product.models import Product
from product.serializers import VersionDetailSerializer, ProductSerializer, VersionSerializer
from project.models import Project
from project.serializers import UserManagedProjectsSerializer, UserJoinedProjectsSerializer
from team.models import Member
from user import serializers
from user.models import VerifCode
from user.permissions import IsOwnerOrReadOnly

# functions
from functions import time_utils

User = get_user_model()


# 登录
class LoginView(TokenObtainPairView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # 成功登录后更新last_login
        user = self.request.user
        if user.is_authenticated:
            user.last_login = time_utils.get_current_time()
            user.save(update_fields=['last_login'])

        return response


class VerifCodeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VerifCodeSerializer
    throttle_classes = [AnonRateThrottle, ]  # 限流，限制验证码发送频率
    permission_classes = [AllowAny, ]

    def send_sms_test(self, request, *args, **kwargs):
        mobile_phone = request.data.get("mobile_phone")
        verification_code = request.data.get("verification_code")
        verif_code = VerifCode.create(mobile_phone=mobile_phone, verification_code=verification_code)
        result = {
            "id": verif_code.id,
            "mobile_phone": verif_code.mobile_phone
        }
        return Response(result, status=status.HTTP_200_OK)


# 用于列出或检索用户的视图集
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    # serializer_class = UserSerializer  # 优先使用 get_serializer_class 返回的序列化器
    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        重写get_permissions，实例化并返回此视图需要的权限列表。
        @return: # 返回相应的权限列表
        """
        if self.action == 'create':  # 如果操作是 'create' （对应POST请求，即注册）
            permission_classes = [AllowAny]  # 允许任何人，不需要身份验证
        else:  # 其他操作
            permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]  # 需要用户被认证
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return serializers.UserRegAndPwdChangeSerializer
        else:
            return serializers.UserSerializer

    def perform_destroy(self, instance):
        """
        重写删除方法，改为逻辑删除
        @param instance:
        @return:
        """
        instance.is_deleted = True
        # TODO: 关联项目需要特殊处理
        instance.save()


# ------------------------我管理的项目-------------------------
# 获取特定用户管理的所有项目
class UserManagedProjectsView(APIView):
    def get(self, request, user_id):
        managed_projects = Project.objects.filter(project_creator_id=user_id)
        serializer = UserManagedProjectsSerializer(managed_projects, many=True)
        response_data = serializer.data
        return Response(response_data)


# 特定用户管理的特定项目的详细信息（获取、更新、删除）
class UserManagedProjectDetailView(APIView):
    @staticmethod
    def get_managed_project(user_id, project_id):
        project = Project.objects.filter(id=project_id, project_creator_id=user_id).first()
        if not project:
            raise NotFound("项目未发现或不是项目管理者！")
        return project

    def get(self, request, user_id, project_id):
        project = self.get_managed_project(user_id, project_id)
        serializer = UserManagedProjectsSerializer(project)
        return Response(serializer.data)

    def patch(self, request, user_id, project_id):
        project = self.get_managed_project(user_id, project_id)
        serializer = UserManagedProjectsSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, user_id, project_id):
        project = self.get_managed_project(user_id, project_id)
        project.delete()
        return Response({"success": True, "message": "项目删除成功!"})


# ------------------------我发布的项目产品-------------------------
# 特定用户管理的特定产品的详细信息（获取、更新）
class UserPublishedProductDetailView(APIView):
    @staticmethod
    def get_managed_product(user_id, project_id):
        project = Project.objects.filter(id=project_id, project_creator_id=user_id).first()
        if not project:
            raise NotFound("项目未发现或不是项目管理者！")
        return project

    def get(self, request, user_id, project_id):
        product = Product.objects.get(project_id=project_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def post(self, request, user_id, project_id):
        serializer = VersionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id, project_id):
        serializer = VersionDetailSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ------------------------我加入的项目-------------------------
# 获取特定用户加入的所有项目
class UserJoinedProjectsView(APIView):
    def get(self, request, user_id):
        # 获取符合条件的队伍ID列表
        team_ids = Member.objects.filter(
            user_id=user_id,
            is_leader=0,
            member_status="正常"
        ).values('team_id').distinct()

        # 查询与这些队伍关联的项目
        joined_projects = Project.objects.filter(team__id__in=team_ids)  # 通过team__id__in来筛选与给定队伍ID列表相关联的项目

        # 使用序列化器来序列化数据
        serializer = UserJoinedProjectsSerializer(joined_projects, many=True)
        response_data = serializer.data

        return Response(response_data)


# 特定用户参与的特定项目的详细信息（获取、更新、退出）
class UserJoinedProjectDetailView(APIView):
    # 检查特定用户是否参与该项目
    def get_project(self, user_id, project_id):
        try:
            project = Project.objects.get(
                id=project_id,
                team__member__user_id=user_id,
                team__member__is_leader=0
            )
            return project
        except Project.DoesNotExist:
            return None

    def get(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            serializer = UserJoinedProjectsSerializer(project)
            return Response(serializer.data)
        else:
            return Response({"error": "你是项目管理者 或 还未加入该项目！"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            serializer = UserJoinedProjectsSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "你是项目管理者 或 还未加入该项目！"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            team_member = Member.objects.get(team__project_id=project, user_id=user_id)
            if team_member.is_leader:
                raise PermissionDenied("项目负责人无法退出项目！")
            team_member.delete()
            return Response({"message": "退出成功！"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "你是项目管理者 或 还未加入该项目！"}, status=status.HTTP_404_NOT_FOUND)


