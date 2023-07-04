# django库
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import get_user_model
# rest_framework库
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# app
from project.models import Project
from project.serializers import UserManagedProjectsSerializer, UserJoinedProjectsSerializer, ProjectSerializer
from user.serializers import UserSerializer
from team.models import Team, Member

User = get_user_model()


# 用于列出或检索用户的视图集
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  # 优先使用 get_serializer_class 返回的序列化器
    permission_classes = [IsAuthenticated]

    # # 根据不同的请求, 获得不同的序列化器
    # def get_serializer_class(self):
    #     if self.action == 'unactived':
    #         return UserUnActiveSerializer
    #     else:
    #         return UserSerializer
    #
    # @action(methods=['get'], detail=False)
    # def unactived(self, request, *args, **kwargs):
    #     # 获取查询集, 过滤出未激活的用户
    #     qs = self.queryset.filter(is_active=False)
    #     # 使用序列化器, 序列化查询集, 并且是
    #     ser = self.get_serializer(qs, many=True)
    #     return Response(ser.data)
    #
    # @action(methods=['get'], detail=False)
    # def actived(self, request, *args, **kwargs):
    #     # 获取查询集, 过滤出未激活的用户
    #     qs = self.queryset.filter(is_active=True)
    #     # 使用序列化器, 序列化查询集, 并且是
    #     ser = self.get_serializer(qs, many=True)
    #     return Response(ser.data)

    # def perform_create(self, serializer):
    #     serializer.save()

    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)


# 获取特定用户管理的所有项目
class UserManagedProjectsView(APIView):
    # 获取特定用户管理的所有项目
    def get(self, request, user_id):
        # 获取特定用户管理的所有队伍ID列表
        team_ids = Member.objects.filter(
            user_id_id=user_id,
            is_leader=True,
            member_status="正常"
        ).values('team_id').distinct()

        # 查询与这些队伍关联的项目
        managed_projects = Project.objects.filter(team__id__in=team_ids)

        # 使用序列化器来序列化数据
        serializer = UserManagedProjectsSerializer(managed_projects, many=True)
        response_data = serializer.data

        return Response(response_data)


# 特定用户管理的特定项目的详细信息（获取、更新、删除）
class UserManagedProjectDetailView(APIView):
    # 检查特定用户是否管理该项目
    def get_project(self, user_id, project_id):
        try:
            project = Project.objects.get(
                id=project_id,
                team__member__user_id=user_id,
                team__member__is_leader=True
            )
            return project
        except Project.DoesNotExist:
            return None

    def get(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            serializer = UserManagedProjectsSerializer(project)
            return Response(serializer.data)
        else:
            return Response({"error": "Project not found or user is not the manager."}, status=404)

    def put(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            serializer = UserManagedProjectsSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({"error": "Project not found or user is not the manager."}, status=404)

    def delete(self, request, user_id, project_id):
        project = self.get_project(user_id, project_id)
        if project:
            project.delete()
            return Response({"success": True, "message": "Project deleted successfully!"})
        else:
            return Response({"error": "Project not found or user is not the manager."}, status=404)


# 获取特定用户加入的所有项目
class UserJoinedProjectsView(APIView):
    def get(self, request, user_id):
        # 获取符合条件的队伍ID列表
        team_ids = Member.objects.filter(
            user_id_id=user_id,
            is_leader=False,
            member_status="正常"
        ).values('team_id').distinct()

        # 查询与这些队伍关联的项目
        joined_projects = Project.objects.filter(team__id__in=team_ids)  # 通过team__id__in来筛选与给定队伍ID列表相关联的项目

        # 使用序列化器来序列化数据
        serializer = UserJoinedProjectsSerializer(joined_projects, many=True)
        response_data = serializer.data

        return Response(response_data)


# 登录
class LoginView(View):
    def get(self, request):
        return HttpResponse("LoginView GET")

    def post(self, request):
        return HttpResponse("LoginView POST")


# 退出登录
class LogoutView(View):
    def get(self, request):
        return HttpResponse("LogoutView GET")

    def post(self, request):
        return HttpResponse("LogoutView POST")


# 忘记密码
class ForgetPwdView(View):
    def get(self, request):
        return HttpResponse("ForgetPwdView GET")

    def post(self, request):
        return HttpResponse("ForgetPwdView POST")
