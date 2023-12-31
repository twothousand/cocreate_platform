# -*- coding: utf-8 -*-
"""
@File : gunicorn_config.py
Description: gunicorn 部署配置
@Time : 2023/7/31 13:37
"""
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import multiprocessing
import os

bind = '0.0.0.0:8000'  # 绑定ip和端口号
backlog = 512      # 监听队列
# chdir = '/home/test/server/bin' # gunicorn要切换到的目的工作目录
timeout = 30     # 超时
worker_class = 'sync'  # 使用gevent模式，还可以使用sync 模式，默认的是sync模式
workers = multiprocessing.cpu_count() * 2 + 1     # 进程数
threads = 2  # 指定每个进程开启的线程数
loglevel = 'info'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "./logs/gunicorn_logs/gunicorn_access.log"         # 访问日志文件
errorlog = "./logs/gunicorn_logs/gunicorn_error.log"        # 错误日志文件
