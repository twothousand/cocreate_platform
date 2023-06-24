from django.db import models
from user.models import User
from .conf import *


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 外键关联 用户表(一对多)
    project_id = models.AutoField(primary_key=True, verbose_name='项目ID')
    image = models.ImageField(upload_to='project_images/', verbose_name='项目展示图片', blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name='项目名称')
    desc = models.TextField(verbose_name='项目介绍')
    TAG_CHOICES = PROJECT_TAG_CHOICES
    TYPE_CHOICES = PROJECT_TYPE_CHOICES
    STATUS_CHOICES = PROJECT_STATUS_CHOICES
    tags = models.CharField(max_length=10, choices=TAG_CHOICES, verbose_name='项目标签')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='项目类型')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='项目状态')
    cycles = models.IntegerField(verbose_name="开发周期", blank=True, null=True)
    link = models.URLField(verbose_name='项目地址', blank=True, null=True)
    views = models.IntegerField(default=0, verbose_name='浏览数量')
    likes = models.IntegerField(default=0, verbose_name='点赞数量')
    favorites = models.IntegerField(default=0, verbose_name='收藏数量')
    other_info = models.TextField(blank=True, verbose_name='备注信息')
    post_datetime = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    is_Active = models.BooleanField(default=True, verbose_name="招募状态")  # 只有两个状态 默认True代表招募 False代表关闭招募

    class Meta:
        db_table = "project"
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def __str__(self):
        return str(self.name)
