# -*- coding: utf-8 -*-
"""
@File : time_utils.py
Description: 时间工具类
@Time : 2023/7/11 16:29
"""
import datetime
# django
from django.utils import timezone


def is_within_valid_period(event_time, valid_period=10):
    """
    检查事件是否在有效期内
    @param event_time: 事件发生的时间，应为datetime对象
    @param valid_period: 事件的有效期，单位为分钟，默认为10分钟
    @return: 如果事件在有效期内，返回True，否则返回False
    """
    now = datetime.datetime.now(event_time.tzinfo)
    if now - event_time <= datetime.timedelta(minutes=valid_period):
        return True
    else:
        return False


def get_current_time():
    """
    获取当前时间
    @return:
    """
    return timezone.now()
