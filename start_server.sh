#!/bin/bash

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
NO_COLOR='\033[0m'

## 存储本地更改
#git stash
#if [ $? -eq 0 ]; then
#    echo -e "${GREEN}Local changes stashed successfully.${NO_COLOR}"
#else
#    echo -e "${RED}Failed to stash local changes. Aborting.${NO_COLOR}"
#    exit 1
#fi
#
## 拉取最新的代码
#git checkout dev
#if [ $? -eq 0 ]; then
#    echo -e "${GREEN}Switched to 'dev' branch successfully.${NO_COLOR}"
#else
#    echo -e "${RED}Failed to switch to 'dev' branch. Aborting.${NO_COLOR}"
#    exit 1
#fi
#
#git pull origin dev
#if [ $? -eq 0 ]; then
#    echo -e "${GREEN}Pulled latest changes from 'dev' branch successfully.${NO_COLOR}"
#else
#    echo -e "${RED}Failed to pull latest changes from 'dev' branch. Aborting.${NO_COLOR}"
#    exit 1
#fi
#
## 应用之前存储的更改
#git stash pop
#if [ $? -eq 0 ]; then
#    echo -e "${GREEN}Local changes applied successfully.${NO_COLOR}"
#else
#    echo -e "${RED}Failed to apply local changes. Aborting.${NO_COLOR}"
#    exit 1
#fi
#
# # 激活conda环境
# source activate cocreate_platform
# if [ $? -eq 0 ]; then
#     echo -e "${GREEN}Activated 'cocreate_platform' conda environment successfully.${NO_COLOR}"
# else
#     echo -e "${RED}Failed to activate 'cocreate_platform' conda environment. Aborting.${NO_COLOR}"
#     exit 1
# fi

# 生成静态文件
python manage.py collectstatic --noinput
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Django 静态文件生成成功.${NO_COLOR}"
else
    echo -e "${RED}Django 静态文件生成失败. 中断...${NO_COLOR}"
    exit 1
fi

python manage.py makemigrations && python manage.py migrate
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Django make migrations 成功.${NO_COLOR}"
else
    echo -e "${RED}Django make migrations 失败. 中断...${NO_COLOR}"
    exit 1
fi
# 用gunicorn启动django项目
gunicorn -c gunicorn_config.py cocreate_platform.wsgi:application -D
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Django 启动成功.${NO_COLOR}"
else
    echo -e "${RED}Django 启动失败. 中断...${NO_COLOR}"
    exit 1
fi

tail -f /dev/null

exec "$@"

