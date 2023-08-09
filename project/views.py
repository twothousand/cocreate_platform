# 系统模块
import logging

# django库
from django.db import transaction
from django.db.models import Q
# rest_framework库
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# common
from common.mixins import my_mixins

# app
from .models import Project
from project import serializers
from team.models import Member
from user.permissions import IsOwnerOrReadOnly, IsProjectOwnerOrReadOnly

# 获得一个logger实体对象
logger = logging.getLogger(__name__)


# 自定义分页器
class CustomPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


# 项目增删改查视图集
class ProjectViewSet(my_mixins.CustomResponseMixin, my_mixins.ListCreatRetrieveUpdateModelViewSet):
    queryset = Project.objects.all()

    def get_permissions(self):
        """
        重写get_permissions，实例化并返回此视图需要的权限列表。
        @return: 返回相应的权限列表
        """
        if self.action == 'create':  # 创建项目
            permission_classes = [IsAuthenticated]  # 需要用户被认证
        elif self.action == 'partial_update':  # 修改项目
            permission_classes = [IsProjectOwnerOrReadOnly, IsAuthenticated]  # 需要项目创建者并且用户被认证
        elif self.action == 'destroy':  # 删除项目
            permission_classes = [IsProjectOwnerOrReadOnly, IsAuthenticated]  # 需要项目创建者并且用户被认证
        else:  # 其他操作
            permission_classes = [AllowAny]  # 允许任何人，不需要身份验证
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProjectListSerializer
        if self.action == 'create':
            return serializers.ProjectCreateSerializer
        if self.action == 'partial_update':
            return serializers.ProjectUpdateSerializer
        if self.action == 'retrieve':
            return serializers.ProjectDetailSerializer
        if self.action == 'destroy':
            return serializers.ProjectDeleteSerializer
        else:
            return serializers.ProjectSerializer

    def list(self, request, *args, **kwargs):
        self.custom_message = "获取项目列表成功！"
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.custom_message = "获取项目详细信息成功！"
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['project_creator'] = request.user.id
        self.custom_message = "创建项目成功！"
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.custom_message = "修改项目信息成功！"
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.custom_message = "删除项目成功！"
        return super().destroy(request, *args, **kwargs)

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# 项目的过滤和搜索视图
class ProjectFilterAndSearchView(APIView):
    # 在搜索时使用已过滤的结果集进行搜索操作
    def get(self, request, *args, **kwargs):
        try:
            keyword = self.request.GET.get('keyword')
            industry = self.request.GET.get('industry')
            ai_tag = self.request.GET.get('ai_tag')
            project_type = self.request.GET.get('project_type')
            project_status = self.request.GET.get('project_status')
            model_name = self.request.GET.get('model_name')

            queryset = Project.objects.all()

            # 应用过滤条件
            if project_status:
                queryset = queryset.filter(project_status__icontains=project_status)
            if project_type:
                queryset = queryset.filter(project_type__icontains=project_type)
            if model_name:
                queryset = queryset.filter(model__model_name__icontains=model_name)
            if industry:
                queryset = queryset.filter(industry__industry__icontains=industry)
            if ai_tag:
                queryset = queryset.filter(ai_tag__ai_tag__icontains=ai_tag)

            # 应用搜索条件
            if keyword:
                queryset = queryset.filter(
                    Q(project_name__icontains=keyword) |
                    Q(project_description__icontains=keyword)
                )

            queryset = queryset.order_by('-id')
            # serializer = serializers.ProjectSerializer(queryset, many=True)
            serializer = serializers.ProjectDetailSerializer(queryset, many=True)

            if serializer.data:
                response_data = {
                    'message': '已成功检索到项目！',
                    'data': serializer.data
                }
            else:
                response_data = {
                    'message': '未检索到任何符合的项目！',
                    'data': serializer.data
                }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                'message': str(e),
                'data': []
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 查看特定项目的成员列表
class ProjectMembersView(APIView):
    def get(self, request, project_id):
        try:
            members = Member.objects.filter(team__project_id=project_id, member_status='正常')  # 包含队长
            serializer = serializers.ProjectMembersSerializer(members, many=True)
            response_data = {
                "message": "成功获取项目成员列表！",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            response_data = {
                "message": "找不到指定项目！！！",
                "data": None
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
