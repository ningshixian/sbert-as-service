import json
import requests


def request_sbert(sbert_url, sen_list):
    """请求sbert服务，获取输入文本的嵌入向量。
    """
    headers = {"Content-Type": "application/json"}
    d = json.dumps({"text": sen_list})
    res = requests.post(sbert_url, data=d, headers=headers, timeout=5)  # 默认超时时间5s
    sen_embeddings = res.json().get("sbert_vec")
    return sen_embeddings


if __name__ == "__main__":
    sbert_url = "http://localhost:8096/sbert"
    sen_list = ["你好", "L8Pro屏幕"]
    request_sbert(sbert_url, sen_list)
