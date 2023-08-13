# django库
from django.contrib.auth import get_user_model
# rest_framework
from rest_framework import serializers
# app
from team.models import Team, Member, Application
from function.models import Image

User = get_user_model()

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image  # 假设Image是你的Image模型
        fields = ['image_url']  # 假设Image模型有一个名为image_url的字段

class UserSerializer(serializers.ModelSerializer):
    profile_image = ImageSerializer(read_only=True)  # 不需要指定source参数

    class Meta:
        model = User  # 假设User是你的User模型
        fields = ['id', 'username', 'nickname', 'professional_career', 'biography', 'location', 'profile_image']


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'nickname', 'professional_career', 'biography', 'location', 'profile_image')
#         ref_name = "team_user"

class TeamRecruitmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id','project','team_leader','is_recruitment_open','recruitment_requirements', 'recruitment_end_date', 'recruitment_slots']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        team_leader = validated_data['team_leader']

        team = Team.objects.create(
            project=validated_data['project'],
            team_leader=team_leader,
            is_recruitment_open=validated_data['is_recruitment_open'],
            recruitment_requirements=validated_data['recruitment_requirements'],
            recruitment_end_date=validated_data['recruitment_end_date'],
            recruitment_slots=validated_data['recruitment_slots'],
        )

        # 创建组队招募后，将当前用户添加为成员并设置为队长
        member = Member.objects.create(team=team, user=team_leader, is_leader=True, member_status='正常')
        member.join_date = team.created_at
        member.save()

        return team

    def update(self, instance, validated_data):
        instance.project = validated_data.get('project', instance.project)
        instance.user = validated_data.get('user', instance.team_leader)
        instance.is_recruitment_open = validated_data.get('is_recruitment_open', instance.is_recruitment_open)
        instance.recruitment_requirements = validated_data.get('recruitment_requirements',
                                                               instance.recruitment_requirements)
        instance.recruitment_slots = validated_data.get('recruitment_slots', instance.recruitment_slots)
        instance.recruitment_end_date = validated_data.get('recruitment_end_date', instance.recruitment_end_date)
        instance.save()
        return instance

class TeamApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Application
        fields = ['id', 'user', 'project', 'team', 'application_msg', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Member
        fields = ['id', 'is_leader', 'join_date', 'leave_date', 'member_status', 'created_at', 'team', 'user']
        read_only_fields = ['id', 'created_at']