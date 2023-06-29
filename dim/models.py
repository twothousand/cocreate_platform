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
    industry = models.CharField(max_length=100, verbose_name='行业', choices=[
        ('IT', '信息技术'),
        ('Finance', '金融服务'),
        ('Retail', '零售和批发'),
        ('Manufacturing', '制造业'),
        ('Media', '媒体和娱乐'),
        ('Healthcare', '医疗保健'),
        ('Education', '教育'),
        ('Hospitality', '酒店和旅游'),
        ('Construction', '建筑和房地产'),
        ('Transportation', '交通运输'),
        ('Agriculture', '农业'),
        ('Energy', '能源和公共事业'),
        ('Fashion', '服装和时尚'),
        ('Food', '食品和饮料'),
        ('Sports', '体育和健身'),
        ('Marketing', '市场营销和广告'),
        ('Consulting', '咨询服务'),
        ('Social Media', '社交媒体和网络'),
        ('Environment', '环境保护和可持续发展'),
        ('Culture', '文化艺术和表演')
    ])

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
    ai_tag = models.CharField(max_length=100, verbose_name='AI标签', choices=[
        ('AI_Dialogue', 'AI对话'),
        ('AI_Drawing', 'AI绘画'),
        ('AI_Prompt', 'AI提示词'),
        ('AI_Image_Processing', 'AI图片处理'),
        ('AI_Text_Writing', 'AI文本写作'),
        ('AI_Audio', 'AI音频'),
        ('AI_Video', 'AI视频'),
        ('AI_Content_Detection', 'AI内容检测'),
        ('AI_Office_Tools', 'AI办公工具'),
        ('AI_Programming', 'AI编程')
    ])

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.ai_tag

    class Meta:
        db_table = 'dim_ai_tags'
        verbose_name = 'AI标签'
        verbose_name_plural = verbose_name
