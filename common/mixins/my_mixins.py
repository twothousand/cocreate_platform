# -*- coding: utf-8 -*-
"""
@File : mixins.py
Description: 一些抽象类以及自定义rest_framework配置（在settings.py中）
@Time : 2023/7/20 21:34
"""
# rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response


# ========================== 自定义rest_framework配置 ==========================
def custom_exception_handler(exc, context):
    # 先使用DRF自带的异常处理
    response = exception_handler(exc, context)

    # 扩展的自定义异常处理
    if isinstance(exc, MethodNotAllowed):
        data = {
            'status': status.HTTP_405_METHOD_NOT_ALLOWED,
            'error': {
                'message': '找不到该方法',
                'code': 405
            }
        }
        response = Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWEDstatus.HTTP_405_METHOD_NOT_ALLOWED)

    return response


# ========================== 一些抽象类 ==========================
class CustomResponseMixin:
    """
    Mixin to format the response with 'status' and 'data'
    """

    @staticmethod
    def get_first_error_message(data):
        values = data.values()
        first_value = next(iter(values), None)
        if first_value is not None and isinstance(first_value, list) and len(first_value) > 0:
            return first_value[0]
        else:
            return None

    def handle_exception(self, exc):
        if isinstance(exc, ValidationError):
            response = super().handle_exception(exc)
            return Response({
                "message": self.get_first_error_message(response.data),
                "data": None
            }, status=response.status_code)

        return super().handle_exception(exc)

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK or response.status_code == status.HTTP_201_CREATED:
            response.data = {
                "data": response.data,
                "message": getattr(self, 'custom_message', '请求成功')  # 获取自定义的 message
            }
        return super().finalize_response(request, response, *args, **kwargs)
