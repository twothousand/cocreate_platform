"""
创建user/serializers.py写序列化器

功能一：数据校验，创建/修改数据

在创建数据或者修改数据时校验用户提交的数据是否合法
用户名必须是8位以上，邮箱、手机号是合法的
功能二：序列化

把通过model查询的queryset对象转换成JSON格式
"""
from rest_framework import serializers
# from user.models import User
from django.contrib.auth.models import User


class UserRegSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "password")


# 构建项目序列化器
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User  # 具体对哪个表进行序列化
        fields = '__all__'  # 所有字段
        # fields = ('id', )       # 临时添加字段也需要写在这里
        # exclude = ['id']  # 排除 id 字段
        # read_only_fields = ('',)  # 指定字段为 read_only,


class UserUnActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_active')  # 临时添加字段也需要写在这里
