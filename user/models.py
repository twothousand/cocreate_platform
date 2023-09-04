"""
用户表
user 项目信息表
"""
# 系统模块
import uuid
# django 模块
from django.db import models
from django.contrib.auth.models import AbstractUser
# common
from common.mixins.common_fields import UUIDField
from common.mixins.base_model import BaseModel
# app
from function.models import Image


# 用户表
class User(AbstractUser, BaseModel):
    """
    用户模型
    """
    id = UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="用户id")
    username = models.CharField(max_length=11, unique=True, verbose_name="手机号码")
    # 继承django自带的AbstractUser类后，不需要password字段，数据库中会自动添加password，且存储加密后的密码
    # password = models.CharField(max_length=50, verbose_name="密码")
    email = models.EmailField(max_length=50, verbose_name='邮箱', blank=True, null=True)
    name = models.CharField(max_length=50, verbose_name='真实姓名', blank=True, null=True)
    nickname = models.CharField(max_length=50, verbose_name='账户名', blank=True, null=True)
    wechat_id = models.CharField(max_length=50, verbose_name='微信号', blank=True, null=True)
    wechat_uuid = models.CharField(max_length=50, verbose_name='微信uuid', blank=True, null=True)
    # phone_number = models.CharField(max_length=50, unique=True, verbose_name='手机号码', blank=True, null=True)
    biography = models.TextField(max_length=300, verbose_name='个人简介', blank=True, null=True)
    professional_career = models.TextField(max_length=50, verbose_name='专业职业', blank=True, null=True)
    location = models.CharField(max_length=50, verbose_name='所在地', blank=True, null=True)
    profile_image = models.ForeignKey(Image, verbose_name='头像', on_delete=models.CASCADE,
                                      default="61766174-6172-2d64-6566-61756c74fd67")
    last_login = models.DateTimeField(verbose_name='最后登录时间', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def get_nickname(self):
        return self.nickname

    @classmethod
    def is_exists_username(cls, username):
        return cls.filter(username=username).exists()

    def __str__(self):
        return f"用户名: {str(self.username)}"

    class Meta:
        db_table = 'user'
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


