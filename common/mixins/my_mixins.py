# -*- coding: utf-8 -*-
"""
@File : mixins.py
Description: 一些抽象类以及自定义rest_framework配置（在settings.py中）
@Time : 2023/7/20 21:34
"""
# 系统模块
import inspect
# rest_framework
from rest_framework import status, mixins, serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, MethodNotAllowed
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
# django
from django.utils import timezone
from django.db import transaction
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
# common
from common.utils import tools


# ========================== 自定义rest_framework配置 ==========================
def custom_exception_handler(exc, context):
    print("===========================")
    # 先使用DRF自带的异常处理
    # response = exception_handler(exc, context)

    # 扩展的自定义异常处理
    if isinstance(exc, MethodNotAllowed):
        data = {
            "message": '找不到该方法',
            "data": None
        }
        response = Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    return response


# ========================== ModelViewSet抽象类 ==========================
class BaseModelViewSet:
    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ListCreatRetrieveUpdateModelViewSet(BaseModelViewSet,
                                          mixins.ListModelMixin,
                                          mixins.CreateModelMixin,
                                          mixins.RetrieveModelMixin,
                                          mixins.UpdateModelMixin,
                                          GenericViewSet):
    """
    list(), create(), update(), partial_update()
    """
    pass


class CreatRetrieveUpdateModelViewSet(BaseModelViewSet,
                                      mixins.CreateModelMixin,
                                      mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      GenericViewSet):
    """
    create(), update(), partial_update()
    """
    pass


class CreatModelViewSet(BaseModelViewSet,
                        mixins.CreateModelMixin,
                        GenericViewSet):
    """
    create()
    """
    pass


class RetrieveUpdateListModelViewSet(BaseModelViewSet,
                                     mixins.UpdateModelMixin,
                                     ReadOnlyModelViewSet):
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


class LoggerMixin:
    def get_request_logger_message(self, request, request_data):
        """
        获得request日志输出（如果有特别的日志输出可以重写方法）
        @param request:
        @param request_data:
        @return:
        """
        class_name = self.__class__.__name__
        method_name = inspect.stack()[1][3]  # 获取调用函数的名称
        return "%s::%s , user_id=[%s], request.data = %s " % (class_name, method_name, request.user.id, request_data)

    def get_response_logger_message(self, request, response_data):
        """
        获得response日志输出（如果有特别的日志输出可以重写方法）
        @param request:
        @param response_data:
        @return:
        """
        class_name = self.__class__.__name__
        method_name = inspect.stack()[1][3]  # 获取调用函数的名称
        return "%s::%s , user_id=[%s], response.data = %s " % (class_name, method_name, request.user.id, response_data)

    def log_request(self, view_instance, logger, request, get_request_logger_message=None):
        # 处理敏感数据
        request_data = tools.sanitize_data(request.data.copy())
        # 使用提供的函数或者默认的函数来生成日志信息
        if get_request_logger_message is None:
            get_request_logger_message = self.get_request_logger_message
        logger_message = get_request_logger_message(request, request_data)
        logger.info(logger_message)

    def log_response(self, view_instance, logger, request, response, get_response_logger_message=None):
        # 处理敏感数据
        response_data = tools.sanitize_data(response.data.copy())
        if get_response_logger_message is None:
            get_response_logger_message = self.get_response_logger_message
        logger_message = get_response_logger_message(request, response_data)
        print(logger_message)
        logger.info(logger_message)


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
