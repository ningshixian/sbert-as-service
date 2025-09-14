import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import sys
import time
import traceback
from typing import Union, Optional
from functools import wraps
from fastapi import FastAPI
from starlette.requests import Request
from pydantic import BaseModel, validator
from sentence_transformers import SentenceTransformer
import torch
import setting
import helpers

torch.set_num_threads(1)  # 线程并行计算时候所占用的线程数，这个可以用来限制 PyTorch 所占用的 CPU 数目；
sys.path.append(r"../utils_toolkit")
# import LogDecorator

"""
# 推荐启动方式 main指当前文件名字 app指FastAPI实例化后对象名称
uvicorn sbert_server:app --host 0.0.0.0 --port 8096 --workers 1 --limit-concurrency 50

# Uvicorn 为单进程的 ASGI server ，而 Gunicorn 是管理运行多个 Uvicorn ，以达到并发与并行的最好效果。
gunicorn sbert_server:app -b 0.0.0.0:8096 -w 1 --threads 100 -k uvicorn.workers.UvicornWorker
"""

app = FastAPI()
# logger = LogDecorator.init_logger(setting.log_file)  # 日志封装类

print("初始化sbert....")
# # Multi-Process / Multi-GPU Encoding 使用多进程来处理请求-CPU占用率会到达100%！
# # You can encode input texts with more than one GPU (or with multiple processes on a CPU machine). 
# # For an example, see: https://github.com/UKPLab/sentence-transformers/tree/master/examples/applications/computing-embeddings/computing_embeddings_mutli_gpu.py
# sbert = SentenceTransformer(setting.sbert_path, device='cpu')  # device='cuda'
# pool = sbert.start_multi_process_pool(target_devices=['cpu']*4) # CUDA若不可用，默认启用4个CPU
sbert = SentenceTransformer(setting.sbert_path)  # device='cuda'
pool = sbert.start_multi_process_pool() # Start the multi-process pool on all available CUDA devices


class Item(BaseModel):
    text: Union[list, str]


@app.post("/sbert")
def main(request: Request, item: Item):
    json_data = item.dict()
    text = json_data.get("text")
    start = 1000 * time.time()
    
    try:
        if isinstance(text, list):
            # vec_q = sbert.encode(text, device="cpu", show_progress_bar=False)  # 极度消耗CPU！
            vec_q = sbert.encode_multi_process(text, pool)
            count = len(text)
        else:
            # vec_q = sbert.encode([text], device="cpu", show_progress_bar=False)  # 极度消耗CPU！
            vec_q = sbert.encode_multi_process([text], pool)
            count = 1
        
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        end = 1000 * time.time()
        # logger.info("sbert ok!\t共计{}条数据\t耗时{}ms".format(count, round(end-start, 2)))
    except Exception as e:
        # logger.error(traceback.format_exc())
        # 钉钉推送错误消息
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print(
            str(t)
            + "\n"
            + f"sbert服务异常: {request.url}"
            + "\n"
            + f"Args: {item.text}"
            + "\n"
            + f"耗时: {1000 * time.time() - start}ms"
            + "\n"
            + f"错误信息: {repr(e)}"
        )
        #Optional: Stop the proccesses in the pool
        sbert.stop_multi_process_pool(pool)
        raise Exception("sbert服务异常: {}".format(e))
    
    # print(type(vec_q))  # <class 'numpy.ndarray'>
    return {"sbert_vec": vec_q.tolist()}
