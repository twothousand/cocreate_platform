"""
在这个示例中，我们继承了ModelSerializer，并指定了TeamMember模型作为序列化的模型。

member_name字段和team_name字段是只读字段，它们源自member.username和team.name，用于在序列化过程中显示成员和队伍的名称。这样，当我们返回序列化的数据时，可以在member_name和team_name字段中看到对应的值。

is_approved字段是可写字段，用于表示队伍成员是否已经被审核通过。
"""
from rest_framework import serializers
from team.models import Team, Member, Application

class TeamSerializer(serializers.ModelSerializer):
    team_leader_id = serializers.ReadOnlyField(source='team_leader_id.username')

    class Meta:
        model = Team
        fields = ['team_name', 'team_leader_id']

    # TODO
    def create(self, validated_data):
        project_id = self.context['request'].user.id
        team_leader = self.context['request'].user.id
        print("team_leader, project_id", team_leader, project_id)
        team = Team.objects.create(team_leader_id=team_leader, project_id=project_id, **validated_data)
        return team


class MemberSerializer(serializers.ModelSerializer):
    member_name = serializers.ReadOnlyField(source='member.username')
    team_name = serializers.ReadOnlyField(source='team.name')

    class Meta:
        model = Member
        fields = ['id', 'member_name', 'team_name', 'is_approved']



class TeamRecruitmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id','project','team_leader','is_recruitment_open','recruitment_requirements', 'recruitment_end_date']
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
        )

        # 创建组队招募后，将当前用户添加为成员并设置为队长
        member = Member.objects.create(team=team, user=team_leader, is_leader=True, member_status='正常')
        member.join_date = team.created_at
        member.save()

        return team

    def update(self, instance, validated_data):
        instance.project = validated_data.get('project', instance.project)
        instance.is_recruitment_open = validated_data.get('is_recruitment_open', instance.is_recruitment_open)
        instance.recruitment_requirements = validated_data.get('recruitment_requirements',
                                                               instance.recruitment_requirements)
        instance.recruitment_end_date = validated_data.get('recruitment_end_date', instance.recruitment_end_date)
        instance.save()
        return instance

class TeamApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'user', 'project', 'team', 'application_msg', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'is_leader', 'join_date', 'leave_date', 'member_status', 'created_at', 'team', 'user']
        read_only_fields = ['id', 'created_at']