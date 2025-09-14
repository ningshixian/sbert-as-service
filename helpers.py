import requests
import json


def dingding(msg, url):
    """钉钉-告警推送"""
    headers = {"Content-Type": "application/json;charset=utf-8"}
    json_text = {
        "msgtype": "text",
        "text": {"content": "报警 " + msg},
        "at": {"atMobiles": [""], "isAtAll": False},
    }
    requests.post(url, json.dumps(json_text), headers=headers)


def test_api():
    url = "http://127.0.0.1:8096/sbert"
    headers = {'Content-Type': 'application/json'}
    d = json.dumps({"text": ["对话", "打扫房间"]})
    res = requests.post(url, data=d, headers=headers)
    sen_embeddings = res.json()
    print(sen_embeddings.get("sbert_vec"))
    print(type(sen_embeddings))
    print(res.status_code)

# test_api()