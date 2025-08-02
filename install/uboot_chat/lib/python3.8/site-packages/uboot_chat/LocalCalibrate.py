import sys
import requests
import json
import re
from queue import Queue
from datetime import datetime


# server_url = 'http://192.168.0.106:8080/rkllm_chat'
ip = "192.168.0.107"
# Create a session object.
session = requests.Session()
session.keep_alive = False  # Close the connection pool to maintain a long connection.
adapter = requests.adapters.HTTPAdapter(max_retries=5)
session.mount('https://', adapter)
session.mount('http://', adapter)

HISTORY_MAX = 2  # 上下文的最大数量
GPT_role = "你是语音识别校准器。现在有一段客户对酒店机器人说的话，由于语音识别的准确率不高，你对那段话进行校准，并直接返回校准后的句子。"


class History:
    def __init__(self, max_size=10):
        self.max_size = max_size
        self.contain = []

    def update(self, data):
        self.contain.append(data)
        if len(self.contain) > self.max_size:
            self.contain = self.contain[1:]



class CalibratorGPT:
    def __init__(self, ip=ip):
        self.history = History(HISTORY_MAX)
        self.system_content = GPT_role  
        self.url = f"http://{ip}:8080/rkllm_chat"
        self.history.update({"role":"user", "content":"请带我去3号房间"})
        self.history.update({"role":"user", "content":"现在湿度是多少"})
        print('<-CalibratorGPT Working...->')

    def contact(self, user_msg: str):
        messages = [{"role":"system", "content":self.system_content}]
        for msg in self.history.contain:
            messages.append(msg)
        user_chatMessage = {"role":"user", "content":user_msg}
        messages.append(user_chatMessage)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'not_required'
        }
        data = {
            "model": 'Local model',
            "messages": messages,
            "stream": False,
            "enable_thinking": False,
            "tools": []
        }
        try:
            # Send a POST request
            responses = session.post(self.url, json=data, headers=headers, stream=False, verify=False)
        except requests.exceptions.ConnectionError:
            print("<-Local Model: 主机已离线->")
            return ""

        # Parse the response
        if responses.status_code == 200:
            server_answer = json.loads(responses.text)["choices"][-1]["message"]["content"]
            return server_answer.replace("<tool_call>", "").replace("</tool_call>", "").strip()
        else:
            print("Error:", responses.text)
            return ""
    
    def end(self):
        print('<-LocalGPT END->')
        


if __name__ == "__main__":
    C = CalibratorGPT("192.168.108.134")
    while True:
        question = input('我:')
        if question:
            print(C.contact(question))