FROM python:3.9.17
LABEL authors="puppet"

# 1.安装系统插件
# COPY ./sources.list /etc/apt/
RUN apt-get update && apt-get install -y vim

# 2.升级pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade pip

# 容器内创建 myproject 文件夹
ENV APP_HOME=/var/www/admin/cocreate_platform
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# 将当前目录加入到工作目录中（. 表示当前目录）
ADD . $APP_HOME
RUN pip install -r $APP_HOME/requirements.txt
RUN pip install gunicorn

# 给start.sh可执行权限
RUN chmod +x ./start_server.sh

ENTRYPOINT /bin/bash ./start_server.sh