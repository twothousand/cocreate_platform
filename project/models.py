from django.db import models
from user.models import User
from .conf import *


class Project(models.Model):
    project_creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="项目创建者")  # 外键关联 用户表(一对多)
    project_id = models.AutoField(primary_key=True, verbose_name='项目ID')
    project_name = models.CharField(max_length=100, verbose_name='项目名称')
    project_description = models.TextField(verbose_name='项目描述')
    project_tags = models.CharField(max_length=20, choices=PROJECT_TAG_CHOICES, verbose_name='项目标签')
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, verbose_name='项目类型')
    project_status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, verbose_name='项目状态')
    project_cycles = models.IntegerField(verbose_name="开发周期", blank=True, null=True)
    project_source_link = models.URLField(verbose_name='项目开源链接', blank=True, null=True)
    project_display_link = models.URLField(verbose_name='项目展示链接', blank=True, null=True)
    project_views = models.IntegerField(default=0, verbose_name='浏览数量')
    project_likes = models.IntegerField(default=0, verbose_name='点赞数量')
    project_favorites = models.IntegerField(default=0, verbose_name='收藏数量')
    project_other_info = models.TextField(verbose_name='其它补充信息', blank=True, null=True)
    project_images = models.ImageField(upload_to='project_images/', verbose_name='项目展示图片', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "project"
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def __str__(self):
        return str(self.project_name)
