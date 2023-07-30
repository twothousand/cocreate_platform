"""
维度信息表
dim_model 模型维度表
dim_industry 行业维度表
dim_ai_tags AI标签维度表
"""
from django.db import models
from common.mixins.base_model import BaseModel


# 模型维度表
class Model(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='模型ID')
    model_name = models.CharField(max_length=20, verbose_name='模型名称')
    model_type = models.CharField(max_length=20, verbose_name='模型类型')
    model_source = models.CharField(max_length=50, verbose_name='模型归属')
    model_description = models.CharField(max_length=255, verbose_name='模型描述')
    is_open_source = models.BooleanField(verbose_name='是否开源', default=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.model_name

    class Meta:
        db_table = 'dim_model'
        verbose_name = '模型'
        verbose_name_plural = verbose_name


# 行业维度表
class Industry(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='行业ID')
    industry = models.CharField(unique=True, max_length=50, verbose_name='行业标签')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.industry

    class Meta:
        db_table = 'dim_industry'
        verbose_name = '行业'
        verbose_name_plural = verbose_name


# AI标签维度表
class AITag(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='AI标签ID')
    ai_tag = models.CharField(unique=True, max_length=50, verbose_name='AI标签')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.ai_tag

    class Meta:
        db_table = 'dim_ai_tags'
        verbose_name = 'AI标签'
        verbose_name_plural = verbose_name


# 图片表
class Image(BaseModel):
    id = models.AutoField(primary_key=True, verbose_name='图片ID')
    image_url = models.URLField(unique=True, verbose_name='图片链接')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.image_url

    class Meta:
        db_table = 'image'
        verbose_name = '图片'
        verbose_name_plural = verbose_name


# 获取模型维度表
def get_model():
    return Model.objects.all().values('id', 'model_name')


# 获取行业维度表
def get_industry():
    return Industry.objects.all().values('id', 'industry')


# 获取AI标签维度表
def get_ai_tag():
    return AITag.objects.all().values('id', 'ai_tag')
