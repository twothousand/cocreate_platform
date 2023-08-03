"""
产品信息表
feedback 反馈表
"""
# 系统模块
import uuid
# django库
from django.db import models
from django.contrib.auth import get_user_model
# common
from common.mixins.common_fields import UUIDField
from common.mixins.base_model import BaseModel

User = get_user_model()


# 反馈表
class Feedback(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='反馈ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联用户')
    FEEDBACK_CHOICES = (
        ('加入我们', '加入我们'),
        ('意见建议', '意见建议'),
    )
    feedback_type = models.CharField(max_length=50, choices=FEEDBACK_CHOICES, verbose_name='反馈类型', default="主动创建")
    feedback_email = models.CharField(max_length=50, blank=True, verbose_name='反馈邮箱')
    feedback_content = models.TextField(blank=False, verbose_name='反馈内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    def __str__(self):
        return f"反馈ID: {self.id}"

    class Meta:
        db_table = 'feedback'
        verbose_name = '反馈建议'
        verbose_name_plural = verbose_name
