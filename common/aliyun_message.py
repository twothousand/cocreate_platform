# -*- coding: utf-8 -*-
"""
@File : aliyun_message.py
Description: 阿里云云短信服务
@Time : 2023/7/11 12:58
"""
# 系统模块
import json
# 短信服务模块
from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi.models import Config
from alibabacloud_dysmsapi20170525.models import SendSmsRequest
from alibabacloud_tea_util.models import RuntimeOptions
# common
from common.config import aliyun_sms_access_key_id, aliyun_sms_access_key_secret


class AliyunSMS:
    # TODO: 申请后都要换掉
    access_key_id = aliyun_sms_access_key_id
    access_key_secret = aliyun_sms_access_key_secret
    endpoint = "dysmsapi.aliyuncs.com"
    sign_name = "阿里云短信测试"
    template_code = "SMS_154950909"

    def __init__(self):
        self.config = Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            endpoint=self.endpoint
        )

    def send_msg(self, phone: str, code: str):
        """
        发送验证码
        @param phone: 手机号
        @param code: 验证码
        @return:
        """
        # 创建客户端
        client = Client(self.config)
        # 创建短信请求对象
        send_sms_request = SendSmsRequest(
            phone_numbers=phone,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param=json.dumps({"code": code})
        )
        # 设置允许时间选项
        runtime = RuntimeOptions()
        # 发送短信
        try:
            res = client.send_sms_with_options(send_sms_request, runtime)
            if res.body.code == "OK":
                return {"code": "OK", "message": "短信发送成功"}
            else:
                return {"code": "NO", "error": res.body.message}
        except Exception as e:
            return {"code": "NO", "error": "短信发送失败"}


if __name__ == '__main__':
    aliyun_sms = AliyunSMS()
    print(aliyun_sms.send_msg(phone="", code="435643"))
