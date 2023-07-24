from rest_framework import serializers
from .models import Project
from team.models import Member


# 项目序列化器
class ProjectSerializer(serializers.ModelSerializer):
    model = serializers.StringRelatedField()
    industry = serializers.StringRelatedField()
    ai_tag = serializers.StringRelatedField()
    project_creator = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Project
        fields = "__all__"


# 获取特定用户管理的所有项目
class UserManagedProjectsSerializer(serializers.ModelSerializer):
    """
        项目封面(考虑流量，暂不获取)、项目名称、项目简介、成员数(从队伍成员表取，暂不获取)
        以及一个”管理项目“的按钮（直接通过项目名称点进去即可） 和一个“删除项目“的按钮
        “删除项目“ 需要再次弹框确认，才能进行删除（不常用，放到项目里边比较好）
    """

    model = serializers.StringRelatedField()
    industry = serializers.StringRelatedField()
    ai_tag = serializers.StringRelatedField()
    project_creator = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    project_views = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = '__all__'


# 获取特定用户加入的所有项目
class UserJoinedProjectsSerializer(serializers.ModelSerializer):
    project_creator_name = serializers.CharField(source='project_creator.name', read_only=True)

    class Meta:
        model = Project
        fields = ("id", "project_creator_name", "project_description", "project_name", "project_type", "project_status",
                  "project_cycles")


# 获取项目成员列表
class ProjectMembersSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField(source='team.team_name')
    username = serializers.ReadOnlyField(source='user.username')
    name = serializers.ReadOnlyField(source='user.name')
    user_id = serializers.ReadOnlyField(source='user.id')
    professional_career = serializers.ReadOnlyField(source='user.professional_career')
    location = serializers.ReadOnlyField(source='user.location')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Member
        fields = ['team_name', 'is_leader', 'member_status', 'user_id', 'username', 'name', 'professional_career',
                  'location', 'email']
