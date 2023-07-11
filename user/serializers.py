"""
创建user/serializers.py写序列化器

功能一：数据校验，创建/修改数据

在创建数据或者修改数据时校验用户提交的数据是否合法
用户名必须是8位以上，邮箱、手机号是合法的
功能二：序列化

把通过model查询的queryset对象转换成JSON格式
"""
# rest_framework库
from rest_framework import serializers
# django库
from django.contrib.auth import get_user_model

User = get_user_model()


# 构建项目序列化器
class UserSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     """
    #     重写用户注册的post方法
    #     @param validated_data:
    #     @return:
    #     """
    #     user = super(UserSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    class Meta:
        model = User  # 具体对哪个表进行序列化
        fields = ["id", "username", "email", "profile_image", "location", "biography", "nickname"]
        # fields = ('id', )       # 临时添加字段也需要写在这里
        # exclude = ['id']  # 排除 id 字段
        # read_only_fields = ('',)  # 指定字段为 read_only,


class UserUnActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_active')  # 临时添加字段也需要写在这里
