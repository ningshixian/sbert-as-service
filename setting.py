# -*- coding: utf-8 -*-
import os

"""用来作变量和常量的初始化"""

# 钉钉告警
url = "..."

# sbert相关
sbert_path = "./models/distilbert-multilingual-nli-stsb-quora-ranking"

# log文件的全路径
log_file = "logs/flask_request8096.log"
# 如果不存在定义的日志目录就创建一个
if not os.path.isdir('logs/'):
    os.mkdir('logs/')
