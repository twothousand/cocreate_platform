"""
用户表
user 项目信息表
"""
from django.db import models


# 用户表
class User(models.Model):
    username = models.CharField(max_length=30, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=50, verbose_name="密码")
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    name = models.CharField(max_length=50, verbose_name='真实姓名', blank=True, null=True)
    nickname = models.CharField(max_length=50, verbose_name='昵称', blank=True, null=True)
    phone_number = models.CharField(max_length=50, verbose_name='手机号码', blank=True, null=True)
    biography = models.TextField(max_length=300, verbose_name='个人简介', blank=True, null=True)
    professional_career = models.TextField(max_length=50, verbose_name='专业职业', blank=True, null=True)
    location = models.CharField(max_length=50, verbose_name='所在地', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', verbose_name='头像', blank=True, null=True)
    last_login = models.DateTimeField(verbose_name='最后登录时间', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f"用户名: {str(self.username)}"

    class Meta:
        db_table = 'user'
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
