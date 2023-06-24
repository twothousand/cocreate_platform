import json

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from rest_framework.serializers import Serializer
from rest_framework import permissions
from .serializers import ProjectSerializer


# Create your views here.
class ProjectViewSet(ModelViewSet):  # 继承ModelViewSet类
    # 使用django rest framework 进行get post请求分发，前后端分离，返回json数据
    queryset = Project.objects.all()  # 指明当前视图集所使用的查询集
    serializer_class = ProjectSerializer  # 指明当前视图所使用的序列化器类
    permission_classes = [permissions.IsAuthenticated]


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


# 项目详情页
class ProjectDetailView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):  # 重写get_queryset方法
        project_id = self.request.query_params.get('id')  # 获取请求参数
        return Project.objects.filter(project_id=project_id)  # 返回查询集


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
