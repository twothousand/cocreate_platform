# -*- coding: utf-8 -*-
"""
@File : re_utils.py
Description: 正则匹配公共方法
@Time : 2023/7/16 13:25
"""
import re


def validate_phone(phone):
    """
    验证手机号码是否有效
    @param phone:
    @return:
    """
    return re.match(r"^1(3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8}$", phone)
