# 系统模块
import uuid
# django
from django.db import models
from django.contrib.auth import get_user_model
# common
from common.mixins.base_model import BaseModel
# app
from product.models import Product, Comment, Reply
from project.models import Project

User = get_user_model()


# Create your models here.
class MessageTemplate(BaseModel):
    MESSAGE_TYPE = [
        ("product_like", "产品点赞"),
        ("product_favorite", "产品收藏"),
        ("product_comment", "产品评论"),
        ("product_reply", "产品回复"),
        ("team_application", "组队申请"),
        ("team_audit_result", "组队审核结果"),
        ("team_leader_transfer", "队长转让"),
        ("team_member_removal", "删除队员"),
    ]
    # MESSAGE_TYPE 的用途只在后台管理有用
    # message_template = MessageTemplate(message_type="product_like11", message_template="{sender_nickname}赞了你的产品{product_name}")
    # message_template.full_clean()  # 这将抛出 ValidationError，因为 "product_like11" 不在 MESSAGE_TYPE 的取值范围内
    # message_template.save()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='消息模板ID')
    message_type = models.CharField(choices=MESSAGE_TYPE, max_length=30, verbose_name="消息类型")
    message_template = models.TextField(max_length=1000, null=False, verbose_name="消息模板")

    def __str__(self):
        return f"消息类型: {str(self.message_type)}"

    class Meta:
        db_table = 'message_template'
        verbose_name = "消息模板"
        verbose_name_plural = verbose_name


class Message(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name='项目ID')
    # 如果您有一个 User 对象 user，您可以使用 user.sent_messages.all() 来获取该用户发送的所有消息。
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发送者ID', related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='接收者ID', related_name='received_messages')
    # send_time 等同于 created_at
    # message_type = models.CharField(choices=MESSAGE_TYPE, max_length=30, verbose_name="消息类型")  # MessageTemplate里面有
    # Message.objects.get(id=some_id).message_template.get(id="01904ad9d6b8464d80e11f8962e72ab0").get_message_type_display() 可以获取到对应中文名名称
    message_template = models.ForeignKey(MessageTemplate, on_delete=models.CASCADE, verbose_name="消息模板ID")
    is_read = models.BooleanField(verbose_name="是否已读")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name='对应产品ID', null=True, default=None)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, verbose_name='对应项目ID', null=True, default=None)
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, verbose_name='评论ID', null=True, default=None)
    reply = models.ForeignKey(Reply, on_delete=models.SET_NULL, verbose_name='回复ID', null=True, default=None)

    def get_message_type_display(self):
        """
        从关联的 MessageTemplate 获取 message_type 的可读值。
        """
        return self.message_template.get_message_type_display()

    def get_message_format(self, format_data):
        """
        获取格式化后的message
        @param format_data:  例如：模板中'你已被抱出项目 {project_name}'对应的format_data={"project_name":project_name}
        @return:
        """
        return self.message_template.message_template.format(**format_data)

    class Meta:
        db_table = 'message'
        verbose_name = "消息通知"
        verbose_name_plural = verbose_name
