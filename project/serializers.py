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


class ImageSerializer(serializers.ModelSerializer):
    image_url_name = serializers.CharField(source='image_url')

    class Meta:
        model = Image
        fields = ['id', 'image_url']


# 项目列表序列化器
class ProjectListSerializer(serializers.ModelSerializer):
    # 支持多对多关系的序列化
    model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='model_name')
    industry = serializers.SlugRelatedField(many=True, read_only=True, slug_field='industry')
    ai_tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ai_tag')
    project_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')

    # 招募信息
    recruitment_slots = serializers.SerializerMethodField()
    recruitment_requirements = serializers.SerializerMethodField()
    recruitment_end_date = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'project_images', 'project_name', 'project_description',  # 项目信息
                  'project_status', 'project_type', 'model', 'industry', 'ai_tag',  # 过滤字段
                  'recruitment_slots', 'recruitment_requirements', 'recruitment_end_date',  # 招募信息
                  ]

    def get_recruitment_slots(self, obj):
        team = Team.objects.filter(project=obj).first()
        if team:
            return team.recruitment_slots
        return None

    def get_recruitment_requirements(self, obj):
        team = Team.objects.filter(project=obj).first()
        if team:
            return team.recruitment_requirements
        return None

    def get_recruitment_end_date(self, obj):
        team = Team.objects.filter(project=obj).first()
        if team:
            return team.recruitment_end_date
        return None

    # 根据项目状态过滤
    # def to_representation(self, instance):
    #     project_status = instance.project_status
    #     if project_status not in ["招募中", "开发中"]:
    #         return {}
    #     return super().to_representation(instance)


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
    recruitment_slots = serializers.SerializerMethodField()
    recruitment_requirements = serializers.SerializerMethodField()
    recruitment_end_date = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_recruitment_slots(self, obj):
        team = Team.objects.filter(project=obj).first()
        if team:
            return team.recruitment_slots
        return None

    def get_recruitment_requirements(self, obj):
        team = Team.objects.filter(project=obj).first()
        if team:
            return team.recruitment_requirements
        return None

    def get_recruitment_end_date(self, obj):
        team = Team.objects.filter(project=obj).first()
        if team:
            return team.recruitment_end_date
        return None


# 项目创建序列化器
class ProjectCreateSerializer(serializers.ModelSerializer):
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
        fields = '__all__'  # ['id', 'project_creator']


# 项目更新序列化器 TODO
class ProjectUpdateSerializer(serializers.ModelSerializer):
    # 更新之前先获取原有的数据
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # 获取多对多关系字段
        model = instance.model.all()
        industry = instance.industry.all()
        ai_tag = instance.ai_tag.all()
        project_images = instance.project_images.all()

        # 将多对多关系字段添加到representation中
        representation['model'] = ModelSerializer(model, many=True).data
        representation['industry'] = IndustrySerializer(industry, many=True).data
        representation['ai_tag'] = AITagSerializer(ai_tag, many=True).data
        representation['project_images'] = ImageSerializer(project_images, many=True).data

        return representation

    def update(self, instance, validated_data):
        # 从验证数据中取出模型、行业、AI标签数据
        models_data = validated_data.pop('model', [])
        industries_data = validated_data.pop('industry', [])
        ai_tags_data = validated_data.pop('ai_tag', [])
        project_images_data = validated_data.pop('project_images', [])

        # 更新项目并保存其他字段
        instance = super().update(instance, validated_data)

        # 清空多对多关系字段
        instance.model.clear()
        instance.industry.clear()
        instance.ai_tag.clear()
        instance.project_images.clear()

        # 添加模型到多对多关系字段
        models = Model.objects.filter(model_name__in=models_data)
        instance.model.add(*models)
        industries = Industry.objects.filter(industry__in=industries_data)
        instance.industry.add(*industries)
        ai_tags = AITag.objects.filter(ai_tag__in=ai_tags_data)
        instance.ai_tag.add(*ai_tags)
        # 获取前端传入的图片数据
        project_images = Image.objects.filter(image_url__in=project_images_data)
        instance.project_images.add(*project_images)

        return instance

    class Meta:
        model = Project
        fields = '__all__'  # ['id', 'project_creator']


# 获取特定用户管理的所有项目序列化器
class UserManagedProjectsSerializer(serializers.ModelSerializer):
    """
        项目封面(考虑流量，暂不获取)、项目名称、项目简介、成员数(从队伍成员表取，暂不获取)
        以及一个”管理项目“的按钮（直接通过项目名称点进去即可） 和一个“删除项目“的按钮
        “删除项目“ 需要再次弹框确认，才能进行删除（不常用，放到项目里边比较好）
    """

    # 支持多对多关系的序列化
    # model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='model_name')
    # industry = serializers.SlugRelatedField(many=True, read_only=True, slug_field='industry')
    # ai_tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ai_tag')
    project_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')
    project_creator_name = serializers.CharField(source='project_creator.name', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    # project_views = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ['id', 'project_images', 'project_creator_name', 'is_deleted', 'project_name', 'project_description',
                  'created_at', 'updated_at']


# 获取特定用户管理的具体项目序列化器
class UserManagedProjectDetailSerializer(serializers.ModelSerializer):
    """
        项目封面(考虑流量，暂不获取)、项目名称、项目简介、成员数(从队伍成员表取，暂不获取)
        以及一个”管理项目“的按钮（直接通过项目名称点进去即可） 和一个“删除项目“的按钮
        “删除项目“ 需要再次弹框确认，才能进行删除（不常用，放到项目里边比较好）
    """

    # 支持多对多关系的序列化
    project_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')
    project_creator_name = serializers.CharField(source='project_creator.name', read_only=True)
    model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='model_name')
    industry = serializers.SlugRelatedField(many=True, read_only=True, slug_field='industry')
    ai_tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ai_tag')
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    # project_views = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = '__all__'


# 获取特定用户加入的所有项目序列化器
class UserJoinedProjectsSerializer(serializers.ModelSerializer):
    project_creator_name = serializers.CharField(source='project_creator.name', read_only=True)

    class Meta:
        model = Project
        fields = ("id", "project_creator_name", "project_description", "project_name", "project_type", "project_status",
                  "project_cycles")


# 获取特定用户加入的具体项目序列化器
class UserJoinedProjectDetailSerializer(serializers.ModelSerializer):
    model = serializers.SlugRelatedField(many=True, read_only=True, slug_field='model_name')
    industry = serializers.SlugRelatedField(many=True, read_only=True, slug_field='industry')
    ai_tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ai_tag')
    project_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='image_url')
    project_creator_name = serializers.CharField(source='project_creator.name', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Project
        fields = '__all__'


# 获取项目成员列表序列化器
class ProjectMembersSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField(source='team.team_name')
    username = serializers.ReadOnlyField(source='user.username')
    nickname = serializers.ReadOnlyField(source='user.nickname')
    user_id = serializers.ReadOnlyField(source='user.id')
    professional_career = serializers.ReadOnlyField(source='user.professional_career')
    location = serializers.ReadOnlyField(source='user.location')
    email = serializers.ReadOnlyField(source='user.email')
    profile_image = serializers.SerializerMethodField()

    # profile_image = serializers.SlugRelatedField(source='user.profile_image_id', many=True, read_only=True, slug_field='image_url')

    def get_profile_image(self, instance):
        # Replace 'image_url' with the actual field name representing the image URL in the Image model.
        return instance.user.profile_image.image_url if instance.user.profile_image else None

    class Meta:
        model = Member
        fields = ['team_name', 'username', 'is_leader', 'member_status', 'user_id', 'nickname', 'professional_career',
                  'location', 'email', 'profile_image']
