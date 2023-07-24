# -*- coding: utf-8 -*-
"""
@File : decorators.py
Description: 存放装饰器
@Time : 2023/7/20 23:50
"""
# rest_framework
from rest_framework.exceptions import MethodNotAllowed


def disallow_methods(methods):
    """
    禁用ModelViewSet中的某些方法（暂未使用）
    @param methods:
    @return:
    """
    methods = [m.upper() for m in methods]

    def decorator(view_func):
        def _wrapped_view(view, request, *args, **kwargs):
            if request.method in methods:
                raise MethodNotAllowed(request.method, detail=f"找不到 {request.method} 方法")
            return view_func(view, request, *args, **kwargs)

        return _wrapped_view

    return decorator


def disallow_actions(actions):
    """
    禁用ModelViewSet中的某些action（暂未使用）
    @param methods:
    @return:
    """
    actions = [a.lower() for a in actions]

    def decorator(view_func):
        def _wrapped_view(view, request, *args, **kwargs):
            if hasattr(request, 'action') and request.action in actions:
                raise MethodNotAllowed(request.method, detail=f'Action {request.action} is not allowed')
            return view_func(view, request, *args, **kwargs)

        return _wrapped_view

    return decorator
