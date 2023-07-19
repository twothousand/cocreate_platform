# -*- coding: utf-8 -*-
"""
@File : common_fields.py
Description: Description of your file.
@Time : 2023/7/7 15:25
"""
# 系统模块
import uuid
# django 模块
from django.db import models
# rest_framework 模块
from rest_framework import exceptions


class UUIDField(models.Field):
    """
    支持在数据库后端连接uuid。
    """

    def from_db_value(self, value, expression, connection):  # type:ignore
        return self.to_python(value)

    def db_type(self, connection):
        return 'char(36)'

    def to_python(self, value):
        if value == '':
            return None
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        try:
            return uuid.UUID(value)
        except ValueError as ex:
            raise exceptions.ValidationError(f'{ex} for "{value}"')

    def get_prep_value(self, value):
        if value is None:
            return value
        # 将 UUID 的 '-' 符号去掉
        return str(value)
