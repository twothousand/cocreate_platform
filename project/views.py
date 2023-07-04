# django库
from django.http import HttpResponse
from django.views import View
# rest_framework库
from rest_framework import filters, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
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

    def search(self, request, *args, **kwargs):
        search_term = kwargs.get('keyword')
        print(search_term)
        queryset = self.filter_queryset(self.get_queryset())

        if search_term:
            queryset = queryset.filter(project_name__icontains=search_term) | queryset.filter(
                project_description__icontains=search_term)
            queryset = queryset.order_by('id')
        print(queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


# 项目详情页
class ProjectDetailView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # 重写get_queryset方法
        project_id = self.request.query_params.get('id')  # 获取请求参数
        return Project.objects.filter(project_id=project_id)  # 返回查询集


class ProjectMembersView(APIView):
    def get(self, request, project_id):
        try:
            # 获取指定项目的成员列表
            members = Member.objects.filter(team__project_id=project_id, member_status='正常', is_leader=False)

            # 序列化成员列表数据
            serializer = ProjectMembersSerializer(members, many=True)

            return Response(serializer.data)
        except Member.DoesNotExist:
            return Response(status=404)


# 以rest_framework，按照项目类型搜索项目
class ProjectTypeView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # 重写get_queryset方法
        project_type = self.request.query_params.get('type')  # 获取请求参数
        print("project_type：-----", project_type)
        return Project.objects.filter(type=project_type)  # 返回查询集


# 按照标签搜索项目
class ProjectTagView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # 重写get_queryset方法
        project_tag = self.request.query_params.get('tag')  # 获取请求参数
        print("project_tag：-----", project_tag)
        return Project.objects.filter(tags=project_tag)  # 返回查询集


# 查询阅读量前十的项目
class ProjectViewsTopTen(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.order_by('-views')[:10]


# 查询点赞量前十的项目
class ProjectLikesTopTen(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.order_by('-likes')[:10]


# 查询收藏量前十的项目
class ProjectFavoritesTopTen(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.order_by('-favorites')[:10]
