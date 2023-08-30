# 系统模块
import random
# rest_framework
from rest_framework import serializers

# common
from common.utils import re_utils
from common.utils.aliyun_message import AliyunSMS
from common.mixins import my_mixins
# app
from function.models import Image
from function.models import VerifCode
from function.models import System

class ImageSerializer(serializers.ModelSerializer):
    TYPE_CHOICES = (
        ('avatar', 'avatar'),
        ('project', 'project'),
        ('product', 'product'),
    )
    category = serializers.ChoiceField(choices=TYPE_CHOICES, required=True, allow_blank=True)

    class Meta:
        model = Image
        fields = '__all__'


class VerifCodeSerializer(my_mixins.MyModelSerializer, serializers.ModelSerializer):
    # code_id = serializers.SerializerMethodField()

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
        # 随机生成六位数验证码
        code = VerifCodeSerializer.get_random_code()
        validated_data["verification_code"] = code
        # 发送短信验证码
        aliyun_sms = AliyunSMS()
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

    # def get_code_id(self, obj):
    #     """
    #     将id映射为code_id输出给前端
    #     @param obj:
    #     @return:
    #     """
    #     return int(obj.id)

    class Meta:
        model = VerifCode
        fields = ['mobile_phone']


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('system_page', 'content_name', 'content_name_en', 'content_title', 'system_text', 'system_json',
                  'updated_at')
