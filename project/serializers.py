# django
from django.shortcuts import get_object_or_404
# rest_framework
from rest_framework import serializers
from rest_framework.settings import api_settings
# app
from .models import Project
from team.models import Member, Team
from dim.models import Model, Industry, AITag
from function.models import Image
from common.mixins import my_mixins
from common.utils.aliyun_green import AliyunModeration


# 项目序列化器
class ProjectSerializer(serializers.ModelSerializer):
    # model_name = serializers.SerializerMethodField()
    # industry_name = serializers.SerializerMethodField()
    # ai_tag_name = serializers.SerializerMethodField()
    model = serializers.PrimaryKeyRelatedField(queryset=Model.objects.all(), many=True)
    industry = serializers.PrimaryKeyRelatedField(queryset=Industry.objects.all(), many=True)
    ai_tag = serializers.PrimaryKeyRelatedField(queryset=AITag.objects.all(), many=True)
    project_images = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Project
        fields = "__all__"

    # def get_model_name(self, obj):
    #     return obj.model.model_name
    #
    # def get_industry_name(self, obj):
    #     return obj.industry.industry
    #
    # def get_ai_tag_name(self, obj):
    #     return obj.ai_tag.ai_tag


class ModelSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model_name')

    class Meta:
        model = Model
        fields = ['id', 'model_name']


class IndustrySerializer(serializers.ModelSerializer):
    industry_name = serializers.CharField(source='industry')

    class Meta:
        model = Industry
        fields = ['id', 'industry_name']


class AITagSerializer(serializers.ModelSerializer):
    ai_tag_name = serializers.CharField(source='ai_tag')

    class Meta:
        model = AITag
        fields = ['id', 'ai_tag_name']


# 项目列表序列化器
class ProjectListSerializer(serializers.ModelSerializer):
    # 支持多对多关系的序列化
    model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='model_name')
    industry = serializers.SlugRelatedField(many=True, read_only=True, slug_field='industry')
    ai_tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ai_tag')
    project_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')

    # 招募信息
    team_id = serializers.SerializerMethodField()
    recruitment_slots = serializers.SerializerMethodField()
    recruitment_requirements = serializers.SerializerMethodField()
    recruitment_end_date = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'project_images', 'project_name', 'project_description',  # 项目信息
                  'project_status', 'project_type', 'model', 'industry', 'ai_tag',  # 过滤字段
                  'team_id', 'recruitment_slots', 'recruitment_requirements', 'recruitment_end_date',  # 招募信息
                  ]

    def get_team_id(self, obj):
        team = self.get_team(obj)
        return team.id if team else None

    def get_recruitment_slots(self, obj):
        team = self.get_team(obj)
        return team.recruitment_slots if team else None

    def get_recruitment_requirements(self, obj):
        team = self.get_team(obj)
        return team.recruitment_requirements if team else None

    def get_recruitment_end_date(self, obj):
        team = self.get_team(obj)
        return team.recruitment_end_date if team else None

    def get_team(self, obj):
        return Team.objects.filter(project=obj).first()

    # 根据组队状态过滤项目
    # def to_representation(self, instance):
    #     team = self.get_team(instance)
    #     is_recruitment_open = team.is_recruitment_open if team else False
    #     print("*" * 100, is_recruitment_open)
    #     if not is_recruitment_open:
    #         pass
    #     data = super().to_representation(instance)
    #     return data


# 项目详情序列化器
class ProjectDetailSerializer(serializers.ModelSerializer):
    # 格式化时间
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    # 项目创建者
    project_creator_username = serializers.CharField(source='project_creator.username', read_only=True)
    project_creator_name = serializers.CharField(source='project_creator.name', read_only=True)
    project_creator_nickname = serializers.CharField(source='project_creator.nickname', read_only=True)

    # 支持多对多关系的序列化
    model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='model_name')
    industry = serializers.SlugRelatedField(many=True, read_only=True, slug_field='industry')
    ai_tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ai_tag')
    project_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')

    # 招募信息
    team_id = serializers.SerializerMethodField()
    recruitment_slots = serializers.SerializerMethodField()
    recruitment_requirements = serializers.SerializerMethodField()
    recruitment_end_date = serializers.SerializerMethodField()

    # 返回每个image的id
    project_images_id = serializers.SerializerMethodField()

    def get_project_images_id(self, obj):
        images = obj.project_images.all()
        return [image.id for image in images]

    class Meta:
        model = Project
        fields = '__all__'

    def get_team_id(self, obj):
        team = self.get_team(obj)
        return team.id if team else None

    def get_recruitment_slots(self, obj):
        team = self.get_team(obj)
        return team.recruitment_slots if team else None

    def get_recruitment_requirements(self, obj):
        team = self.get_team(obj)
        return team.recruitment_requirements if team else None

    def get_recruitment_end_date(self, obj):
        team = self.get_team(obj)
        return team.recruitment_end_date if team else None

    def get_team(self, obj):
        return Team.objects.filter(project=obj).first()


# 项目创建序列化器
class ProjectCreateSerializer(serializers.ModelSerializer):
    def validate_project_name(self, value):
        """
        校验项目名称是否违规
        @param value:
        @return:
        """
        AliyunModeration().validate_text_detection("ad_compliance_detection", value)
        return value

    def validate_project_description(self, value):
        """
        校验项目描述是否违规
        @param value:
        @return:
        """
        AliyunModeration().validate_text_detection("ad_compliance_detection", value)
        return value

    def create(self, validated_data):
        # 从验证数据中取出模型、行业、AI标签数据
        models_data = validated_data.pop('model', [])
        industries_data = validated_data.pop('industry', [])
        ai_tags_data = validated_data.pop('ai_tag', [])
        project_images_data = validated_data.pop('project_images', [])

        # 创建项目并保存其他字段
        project = Project.objects.create(**validated_data)

        # 添加模型到多对多关系字段
        models = Model.objects.filter(model_name__in=models_data)
        project.model.add(*models)
        industries = Industry.objects.filter(industry__in=industries_data)
        project.industry.add(*industries)
        ai_tags = AITag.objects.filter(ai_tag__in=ai_tags_data)
        project.ai_tag.add(*ai_tags)

        # 获取前端传入的图片数据
        project_images = Image.objects.filter(image_url__in=project_images_data)
        project.project_images.add(*project_images)

        return project

    class Meta:
        model = Project
        fields = '__all__'


# 项目更新序列化器
class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


# 项目删除序列化器
class ProjectDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


# 获取特定用户管理的所有项目序列化器
class UserManagedProjectsSerializer(serializers.ModelSerializer):
    # 支持多对多关系的序列化
    # model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='model_name')
    # industry = serializers.SlugRelatedField(many=True, read_only=True, slug_field='industry')
    # ai_tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ai_tag')
    project_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')
    project_creator_name = serializers.CharField(source='project_creator.name', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    # project_views = serializers.ReadOnlyField()
    # 返回每个image的id
    project_images_id = serializers.SerializerMethodField()

    def get_project_images_id(self, obj):
        images = obj.project_images.all()
        return [image.id for image in images]

    class Meta:
        model = Project
        fields = ['id', 'project_images', 'project_images_id', 'project_creator_name', 'is_deleted', 'project_name',
                  'project_description', 'created_at', 'updated_at']


# 获取特定用户管理的具体项目序列化器
class UserManagedProjectDetailSerializer(serializers.ModelSerializer):
    # 支持多对多关系的序列化
    project_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')
    project_creator_name = serializers.CharField(source='project_creator.name', read_only=True)
    model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='model_name')
    industry = serializers.SlugRelatedField(many=True, read_only=True, slug_field='industry')
    ai_tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ai_tag')
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    # project_views = serializers.ReadOnlyField()
    # 返回每个image的id
    project_images_id = serializers.SerializerMethodField()

    def get_project_images_id(self, obj):
        images = obj.project_images.all()
        return [image.id for image in images]

    class Meta:
        model = Project
        fields = '__all__'


# 获取特定用户加入的所有项目序列化器
class UserJoinedProjectsSerializer(my_mixins.MyModelSerializer, serializers.ModelSerializer):
    project_creator_name = serializers.CharField(source='project_creator.name', read_only=True)
    project_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')
    # 返回每个image的id
    project_images_id = serializers.SerializerMethodField()

    def get_project_images_id(self, obj):
        images = obj.project_images.all()
        return [image.id for image in images]

    class Meta:
        model = Project
        fields = ["id", "project_creator_name", "project_images", "project_images_id", "project_description",
                  "project_name", "project_type", "project_status", "project_cycles"]


# 获取特定用户加入的具体项目序列化器
class UserJoinedProjectDetailSerializer(my_mixins.MyModelSerializer, serializers.ModelSerializer):
    model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='model_name')
    industry = serializers.SlugRelatedField(many=True, read_only=True, slug_field='industry')
    ai_tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ai_tag')
    project_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')
    project_creator_name = serializers.CharField(source='project_creator.name', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    # 返回每个image的id
    project_images_id = serializers.SerializerMethodField()

    def get_project_images_id(self, obj):
        images = obj.project_images.all()
        return [image.id for image in images]

    class Meta:
        model = Project
        fields = '__all__'


# 获取项目成员列表序列化器
class ProjectMembersSerializer(my_mixins.MyModelSerializer, serializers.ModelSerializer):
    team_id = serializers.ReadOnlyField(source='team.id')
    team_name = serializers.ReadOnlyField(source='team.team_name')
    username = serializers.ReadOnlyField(source='user.username')
    nickname = serializers.ReadOnlyField(source='user.nickname')
    name = serializers.ReadOnlyField(source='user.name')
    user_id = serializers.ReadOnlyField(source='user.id')
    professional_career = serializers.ReadOnlyField(source='user.professional_career')
    location = serializers.ReadOnlyField(source='user.location')
    email = serializers.ReadOnlyField(source='user.email')
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, instance):
        return instance.user.profile_image.image_url if instance.user.profile_image else None

    class Meta:
        model = Member
        fields = ['team_id', 'team_name', 'username', 'is_leader', 'member_status', 'user_id', 'nickname', 'name',
                  'professional_career', 'location', 'email', 'profile_image']
