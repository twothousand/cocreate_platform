# -*- coding: utf-8 -*-
"""
@File : aliyun_message.py
Description: 阿里云云短信服务
@Time : 2023/7/11 12:58
"""
# 系统模块
import json
import logging
# settings
from cocreate_platform.settings import ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET
# 短信服务模块
from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_tea_openapi.models import Config
from alibabacloud_dysmsapi20170525.models import SendSmsRequest
from alibabacloud_tea_util.models import RuntimeOptions
# common
from common.utils.tools import sanitize_phone_number

logger = logging.getLogger(__name__)


class AliyunSMS:
    # TODO: 申请后都要换掉
    access_key_id = ALIBABA_CLOUD_ACCESS_KEY_ID
    access_key_secret = ALIBABA_CLOUD_ACCESS_KEY_SECRET
    endpoint = "dysmsapi.aliyuncs.com"
    sign_name = "阿里云短信测试"
    template_code = "SMS_154950909"

    def __init__(self):
        self.config = Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret,
            endpoint=self.endpoint
        )

    def send_msg(self, mobile_phone: str, verification_code: str):
        """
        发送验证码
        @param mobile_phone: 手机号
        @param verification_code: 验证码
        @return:
        """
        # 创建客户端
        client = Client(self.config)
        # 创建短信请求对象
        send_sms_request = SendSmsRequest(
            phone_numbers=mobile_phone,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param=json.dumps({"code": verification_code})
        )
        # 设置允许时间选项
        runtime = RuntimeOptions()
        logger_mobile_phone = sanitize_phone_number(mobile_phone)
        # 发送短信
        try:
            res = client.send_sms_with_options(send_sms_request, runtime)
            logger.info("AliyunSMS::send_msg, mobile_phone=%s, response=%s" % (logger_mobile_phone, res))
            if res.body.code == "OK":
                return {"status": "success", "message": "验证码发送成功"}
            else:
                return {"status": "failure", "error": res.body.message}
        except Exception as e:
            logger.error("AliyunSMS::send_msg, mobile_phone=%s, error=%s, response=%s" % (logger_mobile_phone, e, res))
            return {"status": "failure", "error": "验证码发送失败"}


if __name__ == '__main__':
    aliyun_sms = AliyunSMS()
    print(aliyun_sms.send_msg(mobile_phone="15812603566", verification_code="435643"))
