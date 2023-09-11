from django.contrib import admin
from .models import Message, MessageTemplate

# Message模型的Admin类
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'get_message_type_display', 'is_read', 'created_at')
    list_filter = ('sender', 'receiver', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'message_template__message_type', 'product__name', 'project__name', 'comment__text', 'reply__text')
    readonly_fields = ('id', 'created_at')

# MessageTemplate模型的Admin类
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ('message_type', 'message_category', 'message_template')
    list_filter = ('message_type', 'message_category')
    search_fields = ('message_type', 'message_category', 'message_template')
    readonly_fields = ('id', 'created_at')

# 注册Admin类
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageTemplate, MessageTemplateAdmin)
