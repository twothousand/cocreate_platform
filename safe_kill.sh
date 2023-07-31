#!/bin/bash
# 安全关闭 gunicorn

# 获取 gunicorn 的进程ID
pids=$(ps -A | grep "gunicorn" | awk '{print $1}')

# 循环杀掉所有获取到的进程
for pid in $pids
do
  echo "Trying to kill gunicorn process ID: $pid"
  kill -SIGTERM $pid
done

# 等待进程结束
sleep 10

# 再次获取还在运行的进程ID
pids=$(ps -A | grep "gunicorn" | awk '{print $1}')

# 如果进程仍然在运行，强制结束它
for pid in $pids
do
  echo "Forcing kill of gunicorn process ID: $pid"
  kill -9 $pid
done
