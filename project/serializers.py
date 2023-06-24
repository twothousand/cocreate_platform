from rest_framework import serializers
from .models import Project


# 构建项目序列化器
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        # fields = ("id", "project_name", "project_desc")
