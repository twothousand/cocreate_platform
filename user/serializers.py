from rest_framework import serializers
from .models import User


# 构建项目序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
