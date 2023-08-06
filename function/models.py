# 系统模块
import uuid
# django 模块
from django.db import models
# common
from common.mixins.common_fields import UUIDField
from common.mixins.base_model import BaseModel
# app



class VerifCode(BaseModel):
    """验证码模型"""
    id = models.AutoField(primary_key=True, verbose_name='验证码ID')
    mobile_phone = models.CharField(verbose_name="手机号码", max_length=11, null=False)
    verification_code = models.CharField(verbose_name="验证码", max_length=6)

    class Meta:
        db_table = 'verifcode'
        verbose_name = "手机验证码"
        verbose_name_plural = verbose_name


# 图片表
class Image(BaseModel):
    # id = models.AutoField(primary_key=True, verbose_name='图片ID')
    id = UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='图片ID')
    image_url = models.URLField(unique=True, verbose_name='图片链接')
    image_path = models.CharField(max_length=200, verbose_name='图片路径', default='')
    category = models.CharField(max_length=200, verbose_name='图片模块', default='uncategorized')
    upload_user = models.CharField(max_length=36, verbose_name='上传图片的用户Id')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.image_url

    class Meta:
        db_table = 'image'
        verbose_name = '图片'
        verbose_name_plural = verbose_name
