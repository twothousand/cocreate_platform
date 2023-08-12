# -*- coding: utf-8 -*-
"""
@File : aliyun_green.py
Description: 内容审核（文本、图片）
@Time : 2023/7/27 9:36
"""
# 系统模块
import json
import logging
# 阿里云内容检测模块
from alibabacloud_green20220302.client import Client as Green20220302Client
from alibabacloud_tea_openapi.models import Config
from alibabacloud_green20220302 import models as green_20220302_models
from alibabacloud_tea_util import models as util_models
# common
from rest_framework import serializers

from cocreate_platform.settings import ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET

logger = logging.getLogger(__name__)


class AliyunModeration:
    access_key_id = ALIBABA_CLOUD_ACCESS_KEY_ID
    access_key_secret = ALIBABA_CLOUD_ACCESS_KEY_SECRET
    endpoint = f'green-cip.cn-shanghai.aliyuncs.com'

    def __init__(self):
        # 更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        self.config = Config(
            # 必填，您的 AccessKey ID,
            access_key_id=self.access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=self.access_key_secret,
            # Endpoint 请参考 https://api.aliyun.com/product/Green
            endpoint=self.endpoint
        )

    def create_client(self) -> Green20220302Client:
        """
        使用config初始化账号Client
        @return: Client
        """
        return Green20220302Client(self.config)

    def text_moderation(self, service, content) -> dict:
        """
        文本审核
        @param service: 可选参数：nickname_detection：用户昵称 chat_detection：聊天互动 comment_detection：动态评论 pgc_detection：教学物料PGC
        @param content: 文本内容
        @return:
        """
        client = self.create_client()
        service_parameters = json.dumps({"content": content})
        text_moderation_request = green_20220302_models.TextModerationRequest(service, service_parameters)
        runtime = util_models.RuntimeOptions()
        try:
            resp = client.text_moderation_with_options(text_moderation_request, runtime)
            logger.info("AliyunModeration::text_moderation, service=%s, service_parameters=%s, response=%s" % (
            service, service_parameters, resp))
            body = resp.body.to_map()
            if body["Code"] == 200:
                if body["Data"]["labels"] == "":
                    return {"status": body["Code"], "code": 1, "message": "文本审核通过"}
                else:
                    reason = '\n违规说明：' + body["Data"]['reason'] if 'reason' in body["Data"] else ''
                    return {"status": body["Code"], "code": -1, "message": "文本含有违规内容"}
            else:
                return {"status": body["Code"], "code": -2, "message": "参数填写错误"}
        except Exception as error:
            logger.error("AliyunModeration::text_moderation, error=%s, response=%s" % (error, resp))
            return {"code": -3, "message": "文本审核失败", "error": error}

    def check_image_result(self, results: list) -> bool:
        """
        检查审核图片的结果
        @param results:
        @return: True：通过  False：不通过
        """
        for result in results:
            if not result.get("Confidence", None):
                continue
            if result["Label"] != "nonLabel" and result["Confidence"] > 90:  # 只要有一个置信度大于90就不通过
                return False
        return True

    def image_moderation(self, service, imageUrl, dataId="") -> dict:
        """
        图片内容审核
        @param service: 可选参数：baselineCheck,profilePhotoCheck
        @param imageUrl: 图片url
        @param dataId: 图片id，默认为""
        @return:
        参考：https://yundun.console.aliyun.com/?spm=5176.8466032.top-nav.4.4e00145000QBvZ&p=cts#/pictureReview/ruleConfig/cn-shanghai
        """
        client = self.create_client()
        service_parameters = json.dumps({"imageUrl": imageUrl, "dataId": dataId})
        image_moderation_request = green_20220302_models.ImageModerationRequest(service, service_parameters)
        runtime = util_models.RuntimeOptions()
        try:
            resp = client.image_moderation_with_options(image_moderation_request, runtime)
            logger.info("AliyunModeration::image_moderation, service=%s, service_parameters=%s, response=%s" % (
            service, service_parameters, resp))
            body = resp.body.to_map()
            if body["Code"] == 200:
                check_res = self.check_image_result(body["Data"]["Result"])
                if check_res:
                    return {"status": body["Code"], "code": 1, "message": "图片审核通过"}
                else:
                    return {"status": body["Code"], "code": -1, "message": "图片含有违规内容"}
            else:
                return {"status": body["Code"], "code": -2, "message": "参数填写错误"}
        except Exception as error:
            logger.error("AliyunModeration::image_moderation, error=%s, response=%s" % (error, resp))
            return {"code": -3, "message": "图片审核失败", "error": error}

    def validate_text_detection(self, service, value):
        """
        校验文本描述是否违规
        @param service:
        @param value:
        @return:
        """
        moderation_res = self.text_moderation(service, value)
        if moderation_res["code"] != 1:
            raise serializers.ValidationError(moderation_res["message"])
        return value


if __name__ == '__main__':
    # s = AliyunModeration()
    print(AliyunModeration().validate_text_detection("ad_compliance_detection", "fuck"))
    # print(s.image_moderation("baselineCheck", ""))
