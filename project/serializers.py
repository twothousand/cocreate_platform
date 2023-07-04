from rest_framework import serializers
from .models import Project
from team.models import Member


# 构建项目序列化器
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        # fields = ("id", "project_name", "project_desc")

    # 创建新项目并将其分配给特定用户
    # 将project_creator_id添加到team_members，并设置is_leader=True
    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        # 将项目创建者添加到团队成员中，并设置为leader
        Member.objects.create(
            project=project,
            user_id=project.project_creator_id,
            is_leader=True
        )
        return project


# 获取特定用户管理的所有项目
class UserManagedProjectsSerializer(serializers.ModelSerializer):
    project_creator_name = serializers.CharField(source='project_creator.username', read_only=True)

    class Meta:
        model = Project
        # fields = ['id', 'project_name', 'project_creator_name', 'project_description']
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.project_description = validated_data.get('project_description', instance.project_description)
        instance.save()
        return instance


# # 创建新项目并将其分配给特定用户
# class CreateProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = "__all__"
#
#     def create(self, validated_data):
#         # 在保存项目之前，可以进行一些额外的处理
#         # 例如，设置默认值、关联其他模型等
#         project = Project.objects.create(**validated_data)
#         return project


# 获取特定用户加入的所有项目
class UserJoinedProjectsSerializer(serializers.ModelSerializer):
    project_creator_name = serializers.CharField(source='project_creator.username', read_only=True)

    class Meta:
        model = Project
        fields = ("id", "project_name", "project_creator_name", "project_description")


# ProjectMembersSerializer的序列化器
class ProjectMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'user_id', 'team_id', 'is_leader', 'member_status']  # 根据你的需要定义字段
