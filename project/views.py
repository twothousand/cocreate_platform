# django库
from django.http import HttpResponse
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
# rest_framework库
from rest_framework import filters, permissions
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# app
from team.models import Member
from .models import *
from .serializers import ProjectSerializer, ProjectMembersSerializer


# GET：列出所有项目，POST：创建新项目
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    search_fields = ['project_name', 'project_description']
    ordering_fields = ['project_name', 'created_at']


# 按关键词搜索项目
class ProjectSearchView(APIView):
    def get(self, request, *args, **kwargs):
        keyword = kwargs.get('keyword')
        if keyword:
            queryset = Project.objects.filter(project_name__icontains=keyword) | \
                       Project.objects.filter(project_description__icontains=keyword)
            queryset = queryset.order_by('id')
            serializer = ProjectSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No keyword provided'})


# 按参数过滤项目(未实现) TODO
class ProjectFilterView(APIView):
    serializer_class = ProjectSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['industry__industry', 'ai_tag__ai_tag', 'project_type', 'project_status',
                        'model__model_name']  # 添加过滤字段

    def get(self, request, *args, **kwargs):
        print("test" * 10)
        queryset = Project.objects.all()
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)


# 项目详情页
class ProjectDetailView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # 重写get_queryset方法
        project_id = self.request.query_params.get('id')  # 获取请求参数
        return Project.objects.filter(project_id=project_id)  # 返回查询集


# 查看特定项目的成员列表
class ProjectMembersView(APIView):
    def get(self, request, project_id):
        try:
            # 获取指定项目的成员列表
            # members = Member.objects.filter(team__project_id=project_id, member_status='正常', is_leader=False)  # 不包含队长
            members = Member.objects.filter(team__project_id=project_id, member_status='正常')  # 包含队长

            # 序列化成员列表数据
            serializer = ProjectMembersSerializer(members, many=True)

            return Response(serializer.data)
        except Member.DoesNotExist:
            return Response(status=404)
