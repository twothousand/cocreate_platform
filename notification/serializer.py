# -*- coding: utf-8 -*-
"""
@File : serializer.py
Description: Description of your file.
@Time : 2023/8/7 17:30
"""
# rest_framework库
from rest_framework import serializers
# app
from notification.models import Message
from user.serializers import UserHyperlinkSerializer


class MessageSerializer(serializers.ModelSerializer):
    message_type = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    sender = UserHyperlinkSerializer()

    class Meta:
        model = Message
        exclude = ['message_template', 'is_deleted', 'is_read']

    def validate(self, attrs):
        request = self.context['request']
        if request.method.lower() == "patch":
            if attrs != {}:
                return serializers.ValidationError({"message": "该请求不需要多余字段参数"})

        return attrs

    def get_message_type(self, obj):
        return obj.get_message_type_display()

    def get_message(self, obj):
        # 获取message_type
        message_type = obj.get_message_type_display()

        # 如果模板中有新增其他字段，则需要添加对应的字段
        sender_nickname = obj.sender.get_nickname() if obj.sender else None
        product_name = obj.product.get_product_name() if obj.product else None
        project_name = obj.project.get_project_name() if obj.project else None

        # 使用format_data_dict来减少if判断
        format_data_dict = {}
        templates = obj.message_template.get_templates()
        # 使用循环生成字典
        for key, template_fields in templates.items():
            temp = {}
            for field in template_fields:
                temp[field] = locals()[field]
            format_data_dict[key] = temp

        # 获取格式化后的message
        message = obj.get_message_format(format_data_dict[message_type])

        return message

    def update(self, instance, validated_data):
        # 改为已读状态
        instance.is_read = True
        instance.save()
        return instance
