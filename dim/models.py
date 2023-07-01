"""
维度信息表
dim_model 模型维度表
dim_industry 行业维度表
dim_ai_tags AI标签维度表
"""
from django.db import models


# 模型维度表
class Model(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='模型ID')
    model_name = models.CharField(max_length=20, verbose_name='模型名称')
    model_type = models.CharField(max_length=20, verbose_name='模型类型')
    model_source = models.CharField(max_length=50, verbose_name='模型归属')
    model_description = models.CharField(max_length=255, verbose_name='模型描述')
    is_open_source = models.BooleanField(verbose_name='是否开源', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.model_name

    class Meta:
        db_table = 'dim_model'
        verbose_name = '模型'
        verbose_name_plural = verbose_name


# 行业维度表
class Industry(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='行业ID')
    industry = models.CharField(unique=True, max_length=50, verbose_name='行业标签')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.industry

    class Meta:
        db_table = 'dim_industry'
        verbose_name = '行业'
        verbose_name_plural = verbose_name


# AI标签维度表
class AITag(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='AI标签ID')
    ai_tag = models.CharField(unique=True, max_length=50, verbose_name='AI标签')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.ai_tag

    class Meta:
        db_table = 'dim_ai_tags'
        verbose_name = 'AI标签'
        verbose_name_plural = verbose_name
