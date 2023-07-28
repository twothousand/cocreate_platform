# -*- coding: utf-8 -*-
"""
@File : mixins.py
Description: 一些抽象类以及自定义rest_framework配置（在settings.py中）
@Time : 2023/7/20 21:34
"""
# rest_framework
from rest_framework import status, mixins, serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
# django
from django.utils import timezone
from rest_framework.viewsets import GenericViewSet
# common
from common.utils import tools


# ========================== 自定义rest_framework配置 ==========================
# def custom_exception_handler(exc, context):
#     print("===========================")
#     # 先使用DRF自带的异常处理
#     response = exception_handler(exc, context)
#
#     # 扩展的自定义异常处理
#     if isinstance(exc, MethodNotAllowed):
#         data = {
#             "message": '找不到该方法',
#             "data": None
#         }
#         response = Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     return response


# ========================== ModelViewSet抽象类 ==========================
class CreatRetrieveUpdateModelViewSet(mixins.CreateModelMixin,
                                      mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      GenericViewSet):
    """
    create(), update(), partial_update()
    """
    pass


class CreatModelViewSet(mixins.CreateModelMixin,
                        GenericViewSet):
    """
    create()
    """
    pass


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
        # ValidationError 是当数据验证失败时抛出的异常。
        if isinstance(exc, ValidationError):
            response = super().handle_exception(exc)
            return Response({
                "message": self.get_first_error_message(response.data),
                "data": None
            }, status=response.status_code)

        # APIException 是 Django REST Framework 中所有异常的基类，这样可以捕获所有从 REST Framework 抛出的异常
        # 由于是基类，一定要放在下面（不知道是什么异常的时候才使用这个）
        if isinstance(exc, APIException):
            response = super().handle_exception(exc)
            return Response({
                "message": str(exc),
                "data": None
            }, status=response.status_code)

        return super().handle_exception(exc)

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == status.HTTP_200_OK or response.status_code == status.HTTP_201_CREATED:
            response.data = {
                "data": response.data,
                # getattr(self, 'custom_message', '请求成功') 访问类变量self.custom_message，如果没有这个变量，则默认为'请求成功'
                "message": getattr(self, 'custom_message', '请求成功')  # 获取自定义的 message
            }
        return super().finalize_response(request, response, *args, **kwargs)


# ========================== 序列化抽象类 ==========================
class SanitizeModelSerializer:

    def to_representation(self, instance):
        """
        处理返回前端的数据（脱敏处理）
        @param instance:
        @return:
        """
        data = super().to_representation(instance)
        username = data.get('username', None)
        if username:
            data['username'] = tools.sanitize_phone_number(data['username'])
        return data


class MyModelSerializer(SanitizeModelSerializer):
    """总的序列化器"""
    pass
