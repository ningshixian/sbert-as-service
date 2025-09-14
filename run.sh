#!/bin/bash

# # 安装：必须组件，使用阿里云源
# pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /app/requirements.txt

conda activate pp

pkill -f "socket8096_detection.py"
pkill -f "gunicorn sbert_server:app"

# 使用gunicorn运行fastapi
nohup python -u socket8096_detection.py > logs/socket.log 2>&1 &
nohup gunicorn sbert_server:app -c configs/gunicorn_config.py > logs/run.log 2>&1 &

lsof -i:8096
printf "\n"
ps -ef | grep socket8096_detection
printf "脚本启动完毕\n"