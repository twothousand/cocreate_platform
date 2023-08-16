# -*- coding: utf-8 -*-
"""
@File : time_utils.py
Description: 时间工具类
@Time : 2023/7/11 16:29
"""
# 系统模块
import datetime
import pytz
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


def get_current_long_timestamp():
    """
    获得当前时间戳，13位毫秒
    @return:
    """
    return int(get_current_time().timestamp() * 1000)


def get_current_timestamp():
    """
    获得当前时间戳，10位秒
    @return:
    """
    return int(get_current_time().timestamp())


def iso_to_beijing(iso_time):
    # 将ISO时间转换为Python的datetime对象
    dt = datetime.datetime.fromisoformat(iso_time.replace('Z', '+00:00'))

    # 获取北京时区对象
    beijing_tz = pytz.timezone('Asia/Shanghai')

    # 将datetime对象转换为北京时间
    beijing_time = dt.astimezone(beijing_tz).date()
    return beijing_time


def iso_before_beijing_today(iso_time):
    try:
        # 将ISO时间字符串转换为时间对象
        iso_datetime = datetime.datetime.fromisoformat(iso_time.replace('Z', '+00:00'))

        # 将ISO时间转换为北京时间
        beijing_datetime = iso_datetime.astimezone(datetime.timezone(datetime.timedelta(hours=8)))

        # 获取当前北京时间日期
        beijing_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).date()

        # 判断ISO时间是否在北京时间之前的同一天
        return beijing_datetime.date() < beijing_now
    except Exception as e:
        print("An error occurred:", e)
        return None

