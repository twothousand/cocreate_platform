"""
产品信息表
product	产品表
product_versions	产品版本表
product_comments	产品评论表
product_comments_reply	产品评论回复表
product_likes	产品点赞表
product_collect	产品收藏表
"""
# 系统模块
import uuid
# django
from django.db import models
from django.contrib.auth import get_user_model
# common
from common.mixins.common_fields import UUIDField
from common.mixins.base_model import BaseModel
# app
from dim.models import Model, Industry, AITag
from function.models import Image
from project.models import Project

User = get_user_model()


# 产品表
class Product(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='产品ID')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='关联项目')
    SOURCE_CHOICES = (
        ('主动创建', '主动创建'),
        ('后台维护', '后台维护'),
    )
    product_source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name='产品来源', default="主动创建")
    product_name = models.CharField(max_length=50, blank=True, verbose_name='产品名称')
    promotional_image = models.ManyToManyField(Image, blank=True, verbose_name='产品宣传图')
    product_description = models.TextField(blank=True, verbose_name='产品简介')
    TYPE_CHOICES = (
        ('学习型', '学习型'),
        ('应用型', '应用型'),
    )
    product_type = models.CharField(max_length=20, choices=TYPE_CHOICES, blank=True, verbose_name='产品类型')
    industry = models.ManyToManyField(Industry, blank=True, verbose_name='行业')
    ai_tag = models.ManyToManyField(AITag, blank=True, verbose_name='AI标签')
    model = models.ManyToManyField(Model, blank=True, verbose_name='使用模型')
    product_display_link = models.URLField(blank=True, null=True, verbose_name='产品展示链接')
    product_display_qr_code = models.ForeignKey(Image, null=True, on_delete=models.CASCADE,
                                                related_name='display_qr_code', verbose_name='产品展示二维码')
    test_group_qr_code = models.ForeignKey(Image, null=True, on_delete=models.CASCADE,
                                           related_name='test_group_qr_code', verbose_name='用户内测二维码')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def get_product_name(self):
        return self.name

    def __str__(self):
        return f"产品名称: {self.name}"

    class Meta:
        db_table = 'product'
        verbose_name = '产品关联项目'
        verbose_name_plural = verbose_name


# 产品版本表
class Version(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='版本ID')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    version_number = models.CharField(max_length=20, verbose_name='版本号', default='1.0.0')
    product_name = models.CharField(max_length=255, blank=True, verbose_name='产品名称')
    promotional_image = models.ManyToManyField(Image, blank=True, verbose_name='产品宣传图')
    product_description = models.CharField(max_length=500, blank=True, verbose_name='产品简介')
    product_type = models.CharField(max_length=100, blank=True, verbose_name='产品类型')
    model = models.ManyToManyField(Model,verbose_name="模型", default="")
    industry = models.ManyToManyField(Industry,verbose_name="行业", default="")
    ai_tag = models.ManyToManyField(AITag,verbose_name="AI标签", default="")
    product_display_link = models.URLField(blank=True, null=True, verbose_name='产品展示链接')
    product_display_qr_code = models.ForeignKey(
        Image,
        null=True,
        on_delete=models.CASCADE,
        related_name='version_display_qr',  # 修改为 'version_display_qr'
        verbose_name='产品展示二维码'
    )

    test_group_qr_code = models.ForeignKey(
        Image,
        null=True,
        on_delete=models.CASCADE,
        related_name='version_test_group_qr',  # 修改为 'version_test_group_qr'
        verbose_name='用户内测二维码'
    )
    def __str__(self):
        return f"版本ID: {self.id}"

    class Meta:
        db_table = 'product_versions'
        verbose_name = '产品版本'
        verbose_name_plural = verbose_name


# 产品评论表
class Comment(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='评论ID')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    comment_content = models.CharField(max_length=255, verbose_name='评论内容')
    from_user_id = models.IntegerField(verbose_name='评论用户ID')

    def __str__(self):
        return f"评论ID: {self.id}"

    class Meta:
        db_table = 'product_comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name


# 产品评论回复表
class Reply(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='回复ID')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='评论')
    # reply_target = models.ForeignKey(ReplyTarget, on_delete=models.CASCADE, verbose_name='回复目标')
    reply_type = models.CharField(max_length=255, verbose_name='回复类型',
                                  choices=[('to_comment', '针对评论的回复'), ('to_reply', '针对回复的回复')])
    reply_content = models.CharField(max_length=255, verbose_name='回复内容')
    from_user = models.ForeignKey(User, related_name='replies_from', on_delete=models.CASCADE, verbose_name='回复用户')
    to_user = models.ForeignKey(User, related_name='replies_to', on_delete=models.CASCADE, verbose_name='目标用户')

    def __str__(self):
        return f"回复ID: {self.id}"

    class Meta:
        db_table = 'product_comments_reply'
        verbose_name = '回复'
        verbose_name_plural = verbose_name


# 产品点赞表
class Like(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='点赞ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    liked_status = models.CharField(max_length=255, verbose_name='点赞状态', choices=[('0', '取消点赞'), ('1', '已点赞')])
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f"点赞ID: {self.id}"

    class Meta:
        db_table = 'product_likes'
        verbose_name = '点赞'
        verbose_name_plural = verbose_name


# 产品收藏表
class Collect(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='收藏ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    collect_status = models.CharField(max_length=255, verbose_name='收藏状态', choices=[('0', '取消收藏'), ('1', '已收藏')])
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f"收藏ID: {self.id}"

    class Meta:
        db_table = 'product_collect'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
