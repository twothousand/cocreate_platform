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
    return re.match(r"^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$", phone)
