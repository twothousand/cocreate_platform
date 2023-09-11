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

    class OperateType(models.TextChoices):
        """操作类型"""
        REGISTER = ('register', '注册')
        RESET_PASSWORD = ('reset_password', '更新密码')
        OTHER = ('other', '其它')

    id = models.AutoField(primary_key=True, verbose_name='验证码ID')
    mobile_phone = models.CharField(verbose_name="手机号码", max_length=11, null=False)
    verification_code = models.CharField(verbose_name="验证码", max_length=6)
    operate_type = models.CharField(max_length=32, choices=OperateType.choices, default=OperateType.OTHER, verbose_name='操作类型')

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


# 系统资料
class System(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='系统资料ID')
    content_name = models.CharField(max_length=50, verbose_name='系统资料名称')
    content_name_en = models.CharField(max_length=50, verbose_name='系统资料名称(英文)')
    content_title = models.CharField(max_length=100, blank=True, null=True, verbose_name='系统资料标题')
    system_page = models.CharField(max_length=100, blank=True, null=True, verbose_name='系统页面')
    system_text = models.TextField(blank=True, null=True, verbose_name='系统资料(文本类型)')  # 存储网页内容，包括Markdown格式和普通文本
    system_json = models.JSONField(blank=True, null=True, verbose_name='系统资料(json类型)')  # 存储JSON信息，图片等
    updated_at = models.DateTimeField(auto_now=True)  # 记录网页最后更新时间

    def __str__(self):
        return str(self.content_name)  # 显示对象时返回资料名字

    class Meta:
        db_table = 'system'
        verbose_name = '系统资料表'
        verbose_name_plural = verbose_name
