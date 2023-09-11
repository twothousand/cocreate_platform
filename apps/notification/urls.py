# -*- coding: utf-8 -*-
"""
@File : urls.py
Description: Description of your file.
@Time : 2023/8/7 17:35
"""
# django 模块
from django.urls import path
# rest_framework 模块
from rest_framework.routers import DefaultRouter
# app
from apps.notification import views

# 自动生成路由方法, 必须使用视图集
# router = SimpleRouter()  # 没有根路由  /user/ 无法识别
router = DefaultRouter()  # 1.有根路由
router.register(r'', views.MessageViewSet, 'message')  # 2.配置路由

urlpatterns = [
path('get_unread_message_count/', views.MessageQueryView.as_view({'get': 'get_unread_message_count'}), name='get_unread_message_count'),
path('get_message_by_type/', views.MessageQueryView.as_view({'get': 'get_message_by_type'}), name='get_message_by_type'),
path('get_message_by_category/', views.MessageQueryView.as_view({'get': 'get_message_by_category'}), name='get_message_by_category'),
]
urlpatterns += router.urls
