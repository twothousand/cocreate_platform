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
        if request.method in permissions.SAFE_METHODS:  # 如果不是拥有者只有读取权限
            return True
        if request.user.is_superuser:  # 如果是超级管理员
            return True
        return obj == request.user
