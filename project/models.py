"""
项目表
project 项目信息表
"""
# 系统模块
import uuid
# django
from django.db import models
from django.contrib.auth import get_user_model
# common
from common.mixins.base_model import BaseModel
from common.mixins.common_fields import UUIDField
# app
from dim.models import Model, Industry, AITag
from project.conf import PROJECT_TYPE_CHOICES, PROJECT_STATUS_CHOICES
from function.models import Image

User = get_user_model()


# 项目信息表
class Project(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='项目ID')
    project_creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="项目创建者")
    model = models.ManyToManyField(Model, verbose_name="模型")
    industry = models.ManyToManyField(Industry, verbose_name="行业")
    ai_tag = models.ManyToManyField(AITag, verbose_name="AI标签")
    project_name = models.CharField(max_length=100, verbose_name='项目名称')
    project_description = models.TextField(verbose_name='项目描述')
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, verbose_name='项目类型')
    project_status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, verbose_name='项目状态')
    project_cycles = models.IntegerField(verbose_name="项目开发周期", blank=True, null=True)
    project_source_link = models.URLField(verbose_name='项目开源链接', blank=True, null=True)
    project_display_link = models.URLField(verbose_name='项目展示链接', blank=True, null=True)
    project_views = models.IntegerField(default=0, verbose_name='项目浏览数量')
    project_other_info = models.TextField(verbose_name='其它补充信息', blank=True, null=True)
    project_images = models.ManyToManyField(Image, blank=True, verbose_name='项目展示图片')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def get_project_name(self):
        return self.project_name

    def __str__(self):
        return f"项目名称: {str(self.project_name)}"

    class Meta:
        db_table = "project"
        verbose_name = '项目信息'
        verbose_name_plural = verbose_name
