# -*- coding: utf-8 -*-
"""
@File : tools.py
Description: Description of your file.
@Time : 2023/7/27 16:44
"""
# 系统模块
import string
# common
from common.utils.re_utils import validate_phone


# ========================================== 处理敏感字段 ==========================================
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


def sanitize_name(name):
    """
    处理姓名，姓名为中文
    @param name:
    @return:
    """
    if len(name) == 2:
        return name[0] + '*'
    else:
        return name[0] + '*' * (len(name) - 2) + name[-1]


def sanitize_token(token):
    return token[:3] + '*' * 4 + token[-4:]


def sanitize_data(data):
    """
    处理敏感数据
    @param data:
    @return:
    """
    # 添加敏感字段，防止log日志泄露导致数据泄露，特殊处理的在下面处理
    sensitive_fields = ['password', 'wechat_id', 'wechat_uuid']
    for field in sensitive_fields:
        if field in data:
            data[field] = '[SENSITIVE DATA]'

    # 特殊处理
    if data.get('username', None):
        data['username'] = sanitize_phone_number(data['username'])
    if data.get('mobile_phone', None):
        data['mobile_phone'] = sanitize_phone_number(data['mobile_phone'])
    if data.get('refresh', None):
        data['refresh'] = sanitize_token(data['refresh'])
    if data.get('access', None):
        data['access'] = sanitize_token(data['access'])

    return data


# ========================================== 工具函数 ==========================================
def extract_keys_from_template(template_str):
    """
    提取格式化字符串中的key
    @param template_str:
    @return: '你已被抱出项目 {project_name}' -> ["project_name"]
    """
    formatter = string.Formatter()
    return [field_name for _, field_name, _, _ in formatter.parse(template_str) if field_name]
