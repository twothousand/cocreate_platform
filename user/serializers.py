"""
创建user/serializers.py写序列化器

功能一：数据校验，创建/修改数据

在创建数据或者修改数据时校验用户提交的数据是否合法
用户名必须是8位以上，邮箱、手机号是合法的
功能二：序列化

把通过model查询的queryset对象转换成JSON格式
"""
# 系统模块
import random
from datetime import timedelta
# rest_framework库
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# django库
from django.contrib.auth import get_user_model
# common
from common.utils.aliyun_message import AliyunSMS
from common.utils import re_utils, time_utils
from common import constant
from common.mixins import my_mixins
# app
from function.models import VerifCode, Image

User = get_user_model()


# =============================================== 公共校验函数 ===============================================


def check_verif_code(mobile_phone: str, verification_code: str) -> (bool, dict):
    """
    校验验证码
    @param mobile_phone: 手机号码
    @param verification_code: 验证码
    @return: 如果验证码有效，返回True，否则返回False
    """
    result = {}
    res = VerifCode.filter(
            verification_code=verification_code,
            mobile_phone=mobile_phone
    ).order_by('-created_at')
    if res.exists():  # 验证码存在
        obj = res[0]
        if obj.is_deleted:
            result["error"] = "验证码已被使用，请重新获取验证码"
            return False, result
        if not time_utils.is_within_valid_period(obj.created_at, valid_period=constant.CAPTCHA_TIMEOUT):
            result["error"] = "验证码已过期，请重新获取验证码"
            return False, result
        obj.is_deleted = True  # 设置为被使用过了
        obj.save()
    else:
        result["error"] = "验证码验证失败，请重新获取验证码"
        return False, result
    return True, result


# =============================================== Serializer ===============================================
class UserLoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField(min_length=11, max_length=11)

    def validate(self, attrs):
        data = super().validate(attrs)
        # TODO 看前端需要什么字段
        data["user_id"] = self.user.id
        data["username"] = self.user.username
        data["nickname"] = self.user.nickname
        profile_image = self.user.profile_image
        data["profile_image"] = profile_image.image_url if profile_image else profile_image

        return data

    # @property
    # def token(self):
    #     # 如果要向令牌添加更多数据
    #     token = super().token
    #
    #     return token

    class Meta:
        model = User
        fields = ["id", "username"]


# 构建项目序列化器
class UserSerializer(my_mixins.MyModelSerializer, serializers.ModelSerializer):
    profile_image = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all())

    def validate_username(self, value):
        """
        验证是否修改了手机号
        @param value:
        @return:
        """
        request = self.context.get("request", None)
        if request and value != request.user.username:
            raise serializers.ValidationError("请通过更换手机绑定的方式修改手机号码！")
        return value

    def get_profile_image(self, obj):
        profile_image = obj.profile_image
        return profile_image.image_url if profile_image else profile_image

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['profile_image'] = self.get_profile_image(instance)
        return response

    class Meta:
        model = User  # 具体对哪个表进行序列化
        fields = ["id", "username", "email", "profile_image", "location", "biography", "nickname", "professional_career", "wechat_id"]
        # fields = ('id', )       # 临时添加字段也需要写在这里
        # exclude = ['id']  # 排除 id 字段
        # read_only_fields = ('id', "username")  # 指定字段为 read_only,


class UserUnActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_active')  # 临时添加字段也需要写在这里


class UserRegAndPwdChangeSerializer(my_mixins.MyModelSerializer, serializers.ModelSerializer):
    """
    用户注册和修改密码Serializer
    """
    verification_code = serializers.CharField(max_length=6, write_only=True)  # write_only=True表示不会序列化输出给前端

    def validate_username(self, value):
        """
        校验手机号码是否有效
        """
        res = re_utils.validate_phone(phone=value)
        if not res:
            raise serializers.ValidationError("无效的手机号码")

        request = self.context.get("request", None)
        if request.method.lower() == "patch" and value != request.user.username:
            raise serializers.ValidationError("请使用账号绑定的手机号码进行验证")
        return value

    def validate(self, data):
        """
        数据校验
        """
        # 校验密码
        if not (6 <= len(data.get('password')) <= 18):
            raise serializers.ValidationError({"password": "密码长度需要在6到18位之间"})

        # 校验验证码
        res, result = check_verif_code(mobile_phone=data.get('username'), verification_code=data.get('verification_code'))
        if not res:
            raise serializers.ValidationError({"verification_code": result["error"]})

        # 弹出无用字段
        data.pop('verification_code')

        return data

    def create(self, validated_data):
        """
        用户注册的POST方法
        @param validated_data:
        @return:
        """
        # 调用父类方法
        user = super(UserRegAndPwdChangeSerializer, self).create(validated_data=validated_data)
        # 调用User父类中的存储密码的方法
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        修改密码PATCH方法
        @param instance:
        @param validated_data:
        @return:
        """
        # 调用父类方法
        user = super(UserRegAndPwdChangeSerializer, self).update(instance=instance, validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'password', 'verification_code']

        extra_kwargs = {
            'username': {
                'validators': [  # 官方文档 validators
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message='该手机号码已注册'
                    )
                ],
            },
            'password': {
                'write_only': True
            },
        }

# 用户搜索序列化器
class UserSearchSerializer(serializers.ModelSerializer):
    # profile_image = serializers.CharField(source='profile_image.image_url', read_only=True)
    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.image_url
        else:
            return None  # 这里返回整个 profile_image 对象或者你想要的其他默认值

    class Meta:
        model = User
        fields = ['id', 'nickname', 'biography', 'professional_career', 'location', 'profile_image']
