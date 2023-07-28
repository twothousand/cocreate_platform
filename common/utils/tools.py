# -*- coding: utf-8 -*-
"""
@File : tools.py
Description: Description of your file.
@Time : 2023/7/27 16:44
"""
from common.utils.re_utils import validate_phone


def sanitize_phone_number(phone):
    """
    处理手机号码
    @param phone:
    @return:
    """
    if validate_phone(phone):
        return phone[:3] + '*' * 4 + phone[-4:]
    else:
        return phone


def sanitize_data(data):
    """
    处理敏感数据
    @param data:
    @return:
    """
    sensitive_fields = ['password']  # 更新敏感字段，特殊处理的在下面处理
    for field in sensitive_fields:
        if field in data:
            data[field] = '[SENSITIVE DATA]'

    # 特殊处理
    if 'username' in data:
        data['username'] = sanitize_phone_number(data['username'])
    return data
