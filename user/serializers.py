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
# rest_framework库
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# django库
from django.contrib.auth import get_user_model
# common
from common.aliyun_message import AliyunSMS
from common import constant
# functions
from functions import time_utils, re_utils
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
    if VerifCode.filter(id=code_id, verification_code=verification_code, mobile_phone=mobile_phone).exists():  # 验证码存在
        obj = VerifCode.get(id=code_id)
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

    def validate(self, attrs):
        data = super().validate(attrs)
        # TODO 看前端需要什么字段
        data['id'] = self.user.id
        data['username'] = self.user.username

        return data

    @property
    def token(self):
        # 如果要向令牌添加更多数据
        token = super().token
        token['username'] = self.user.username

        return token


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
    verification_code = serializers.CharField(max_length=6, write_only=True)  # write_only=True表示不会序列化输出给前端
    code_id = serializers.IntegerField(write_only=True)

    def validate_username(self, value):
        """
        校验手机号码是否有效
        """
        res = re_utils.validate_phone(phone=value)
        if not res:
            raise serializers.ValidationError("无效的手机号码")
        return value

    def validate(self, data):
        """
        数据校验
        """
        # 校验密码
        if not (6 <= len(data.get('password')) <= 18):
            raise serializers.ValidationError({"password": "密码长度需要在6到18位之间"})

        # 校验验证码
        res, result = check_verif_code(mobile_phone=data.get('username'), code_id=data.get('code_id'),
                                       verification_code=data.get('verification_code'))
        if not res:
            raise serializers.ValidationError({"verification_code": result["error"]})

        # 弹出无用字段
        data.pop('verification_code')
        data.pop('code_id')

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
        fields = ['id', 'username', 'password', 'verification_code', 'code_id']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class VerifCodeSerializer(serializers.ModelSerializer):
    code_id = serializers.SerializerMethodField()

    def validate_mobile_phone(self, value):
        """
        校验手机号码是否有效
        @param value:
        @return:
        """
        res = re_utils.validate_phone(phone=value)
        if not res:
            return serializers.ValidationError("无效的手机号码")
        return value

    def create(self, validated_data):
        print("create: ",validated_data)
        # 随机生成六位数验证码
        code = VerifCodeSerializer.get_random_code()
        validated_data["verification_code"] = code
        # 发送短信验证码
        aliyun_sms = AliyunSMS()
        print("create2: ", validated_data)
        res = aliyun_sms.send_msg(**validated_data)
        if res["status"] == "success":
            verif_code = super(VerifCodeSerializer, self).create(validated_data=validated_data)
            return verif_code
        else:
            return serializers.ValidationError(res)

    @staticmethod
    def get_random_code():
        """
        随机生成六位数验证码
        @return:
        """
        code = "".join([str(random.choice(range(10))) for _ in range(6)])
        return code

    def get_code_id(self, obj):
        """
        将id映射为code_id输出给前端
        @param obj:
        @return:
        """
        return int(obj.id)

    class Meta:
        model = VerifCode
        fields = ['code_id', 'mobile_phone']