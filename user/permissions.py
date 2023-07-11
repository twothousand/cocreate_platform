# -*- coding: utf-8 -*-
"""
@File : permissions.py
Description: 自定义权限
@Time : 2023/7/11 09:57
"""
# rest_framework模块
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user
