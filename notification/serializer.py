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


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    def update(self, instance, validated_data):
        # 改为已读状态
        instance.is_read = True
        instance.save()
        return instance
