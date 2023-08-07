# 系统模块
import uuid
# django
from django.db import models
from django.contrib.auth import get_user_model
# common
from common.mixins.base_model import BaseModel

User = get_user_model()


# Create your models here.
class message(BaseModel):
    MESSAGE_TYPE = [
        ("", "")
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='项目ID')
    sender = models.ForeignKey(User, verbose_name='发送者ID')
    receiver = models.ForeignKey(User, verbose_name='接收者ID')
    message_type = models.CharField(choices=MESSAGE_TYPE, max_length=20, verbose_name="消息类型")