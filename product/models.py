"""
产品信息表
product	产品表
product_versions	产品版本表
product_comments	产品评论表
product_comments_reply	产品评论回复表
product_likes	产品点赞表
product_collect	产品收藏表
"""
from django.db import models

from project.models import Project
from user.models import User


# 产品表
class Product(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='产品ID')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='关联项目')
    name = models.CharField(max_length=255, blank=True, verbose_name='产品名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f"产品ID: {self.id}"

    class Meta:
        db_table = 'product'
        verbose_name = '产品'
        verbose_name_plural = verbose_name


# 产品版本表
class Version(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='版本ID')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    version_number = models.CharField(max_length=20, verbose_name='版本号')
    name = models.CharField(max_length=255, blank=True, verbose_name='产品名称')
    promotional_image = models.CharField(max_length=255, blank=True, verbose_name='产品宣传图')
    description = models.CharField(max_length=500, blank=True, verbose_name='产品简介')
    type = models.CharField(max_length=100, blank=True, verbose_name='产品类型')
    industry = models.CharField(max_length=100, blank=True, verbose_name='行业')
    ai_tags = models.CharField(max_length=255, blank=True, verbose_name='AI标签')
    model_ids = models.CharField(max_length=255, verbose_name='模型IDs')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f"版本ID: {self.id}"

    class Meta:
        db_table = 'product_versions'
        verbose_name = '版本'
        verbose_name_plural = verbose_name


# 产品评论表
class Comment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='评论ID')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    comment_content = models.CharField(max_length=255, verbose_name='评论内容')
    from_user_id = models.IntegerField(verbose_name='评论用户ID')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f"评论ID: {self.id}"

    class Meta:
        db_table = 'product_comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name


# 产品评论回复表
class Reply(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='回复ID')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='评论')
    # reply_target = models.ForeignKey(ReplyTarget, on_delete=models.CASCADE, verbose_name='回复目标')
    reply_type = models.CharField(max_length=255, verbose_name='回复类型',
                                  choices=[('to_comment', '针对评论的回复'), ('to_reply', '针对回复的回复')])
    reply_content = models.CharField(max_length=255, verbose_name='回复内容')
    from_user = models.ForeignKey(User, related_name='replies_from', on_delete=models.CASCADE, verbose_name='回复用户')
    to_user = models.ForeignKey(User, related_name='replies_to', on_delete=models.CASCADE, verbose_name='目标用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return f"回复ID: {self.id}"

    class Meta:
        db_table = 'product_comments_reply'
        verbose_name = '回复'
        verbose_name_plural = verbose_name


# 产品点赞表
class Like(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='点赞ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    liked_status = models.CharField(max_length=255, verbose_name='点赞状态', choices=[('0', '取消点赞'), ('1', '已点赞')])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f"点赞ID: {self.id}"

    class Meta:
        db_table = 'product_likes'
        verbose_name = '点赞'
        verbose_name_plural = verbose_name


# 产品收藏表
class Collect(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='收藏ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')
    collect_status = models.CharField(max_length=255, verbose_name='收藏状态', choices=[('0', '取消收藏'), ('1', '已收藏')])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f"收藏ID: {self.id}"

    class Meta:
        db_table = 'product_collect'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
