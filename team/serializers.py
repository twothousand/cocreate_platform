"""
在这个示例中，我们继承了ModelSerializer，并指定了TeamMember模型作为序列化的模型。

member_name字段和team_name字段是只读字段，它们源自member.username和team.name，用于在序列化过程中显示成员和队伍的名称。这样，当我们返回序列化的数据时，可以在member_name和team_name字段中看到对应的值。

is_approved字段是可写字段，用于表示队伍成员是否已经被审核通过。
"""
from rest_framework import serializers
from .models import Member, Team


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
