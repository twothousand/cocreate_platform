"""
创建user/serializers.py写序列化器

功能一：数据校验，创建/修改数据

在创建数据或者修改数据时校验用户提交的数据是否合法
用户名必须是8位以上，邮箱、手机号是合法的
功能二：序列化

把通过model查询的queryset对象转换成JSON格式
"""
# 系统模块
import re
# rest_framework库
from rest_framework import serializers
# django库
from django.contrib.auth import get_user_model
# common
from common import constant
# functions
from functions import TimeUtils
# app
from user.models import VerifCode

User = get_user_model()


# =============================================== 公共校验函数 ===============================================

def check_verif_code(mobile_phone: str, code_id: int, verification_code: str) -> (bool, dict):
    """
    校验验证码
    @param mobile_phone: 手机号码
    @param code_id: 验证码id
    @param verification_code: 验证码
    @return: 如果验证码有效，返回True，否则返回False
    """
    result = {}
    if VerifCode.filter(id=code_id, verif_code=verification_code, mobile_phone=mobile_phone).exists():  # 验证码存在
        obj = VerifCode.get(id=code_id)
        if obj.is_delete:
            result["error"] = "验证码已被使用，请重新获取验证码"
            return False, result
        if not TimeUtils.is_within_valid_period(obj.created_at, valid_period=constant.CAPTCHA_TIMEOUT):
            result["error"] = "验证码已过期，请重新获取验证码"
            return False, result
        obj.is_delete = True  # 设置为被使用过了
        obj.save()
    else:
        result["error"] = "验证码验证失败，请重新获取验证码"
        return False, result
    return True, result

# =============================================== Serializer ===============================================

# 构建项目序列化器
class UserSerializer(serializers.ModelSerializer):
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


class UserRegAndPwdChangeSerializer(serializers.ModelSerializer):
    """
    用户注册和修改密码Serializer
    """
    password_confirmation = serializers.CharField(write_only=True)  # write_only=True表示不会序列化输出给前端
    verification_code = serializers.CharField(max_length=6, write_only=True)
    code_id = serializers.IntegerField(write_only=True)

    def validate_username(self, value):
        """
        校验手机号码是否有效
        """
        res = re.match(r"^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$", value)
        if not res:
            raise serializers.ValidationError("无效的手机号码")
        return value

    def validate(self, data):
        """
        数据校验
        """
        # 校验密码
        if not (6 <= len(data.get('password')) <= 18):
            raise serializers.ValidationError({"password_confirmation": "密码长度需要在6到18位之间"})

        if data.get('password') != data.get('password_confirmation'):
            raise serializers.ValidationError({"password_confirmation": "两次密码不一致"})

        # 校验验证码
        res, result = check_verif_code(mobile_phone=data.get('username'), code_id=data.get('code_id'), verification_code=data.get('verification_code'))
        if not res:
            raise serializers.ValidationError({"verification_code": result["error"]})

        return data

    def create(self, validated_data):
        """
        用户注册的POST方法
        @param validated_data:
        @return:
        """
        validated_data.pop('password_confirmation')
        validated_data.pop('verification_code')
        validated_data.pop('code_id')
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
        validated_data.pop('password_confirmation')
        validated_data.pop('verification_code')
        validated_data.pop('code_id')
        # 调用父类方法
        user = super(UserRegAndPwdChangeSerializer, self).update(instance=instance, validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_confirmation', 'verification_code', 'code_id']
        extra_kwargs = {
            'password': {'write_only': True},
        }


