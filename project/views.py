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
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


# 项目增删改查视图集
class ProjectViewSet(my_mixins.CustomResponseMixin, my_mixins.ListCreatRetrieveUpdateModelViewSet):
    # queryset = Project.objects.all()
    queryset = Project.objects.filter(team__is_recruitment_open=True)  # 只查询招募状态为True的项目
    pagination_class = CustomPagination  # 自定义分页器

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
    pagination_class = CustomPagination  # 自定义分页器

    # 在搜索时使用已过滤的结果集进行搜索操作
    def get(self, request, *args, **kwargs):
        try:
            keyword = self.request.GET.get('keyword')
            industry = self.request.GET.getlist('industry')
            ai_tag = self.request.GET.getlist('ai_tag')
            project_type = self.request.GET.get('project_type')
            project_status = self.request.GET.get('project_status')
            model_name = self.request.GET.getlist('model_name')

            queryset = Project.objects.all()

            # 应用过滤条件
            if project_status:
                queryset = queryset.filter(project_status=project_status)
            if project_type:
                queryset = queryset.filter(project_type=project_type)
            if len(model_name) > 0 and model_name[0] != '':
                queryset = queryset.filter(model__model_name__in=model_name)
            if len(industry) > 0 and industry[0] != '':
                queryset = queryset.filter(industry__industry__in=industry)
            if len(ai_tag) > 0 and ai_tag[0] != '':
                queryset = queryset.filter(ai_tag__ai_tag__in=ai_tag)

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


# 查看特定项目的成员列表，不需要鉴权
class ProjectMembersView(APIView):
    def get(self, request, project_id):
        try:
            members = Member.objects.filter(team__project_id=project_id, member_status='正常')  # 包含队长
            # 队长排在第一位,其他队员按加入时间倒序排列(先加入的排在前面)
            members = members.order_by('-is_leader', 'join_date')
            serializer = serializers.ProjectMembersSerializer(members, many=True)
            response_data = {
                "message": "成功获取项目成员列表！",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "message": "查询错误。",
                "data": str(e)
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

# 查看特定项目的成员列表，需要鉴权
class ProjectTeamMembersView(APIView):
    def get(self, request, project_id):
        try:
            permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]  # 需要用户被认证
            # 检查用户是否在 Member 表中有匹配记录
            user_in_team = Member.objects.filter(user_id=request.user, team__project_id=project_id, member_status='正常').exists()
            print('user_in_team',user_in_team)
            if not user_in_team:
                response_data = {
                    "message": "用户没有队内成员信息查看权限。",
                    "data": None
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)

            members = Member.objects.filter(team__project_id=project_id, member_status='正常')  # 包含队长
            # 队长排在第一位,其他队员按加入时间倒序排列(先加入的排在前面)
            members = members.order_by('-is_leader', 'join_date')
            serializer = serializers.ProjectTeamMembersSerializer(members, many=True)
            response_data = {
                "message": "成功获取项目成员列表！",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "message": "查询错误。",
                "data": str(e)
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
