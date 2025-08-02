import requests
import json
from time import time


# server_url = 'http://192.168.0.106:8080/rkllm_chat'
ip = "127.0.0.1"
# Create a session object.
session = requests.Session()
session.keep_alive = False  # Close the connection pool to maintain a long connection.
adapter = requests.adapters.HTTPAdapter(max_retries=5)
session.mount('https://', adapter)
session.mount('http://', adapter)

HISTORY_MAX = 2  # 上下文的最大数量
# GPT_role = ("你是酒店服务机器人的语音识别校准器。由于语音识别的准确率不高，你需要对句子进行校准，并直接返回校准后的句子。"
#             "例如："
#             "请带我去三号防线。返回：请带我去3号房间"
#             "现在的适度怎么样。返回：现在的湿度怎么样"
# )
GPT_role = ("""你是一名酒店服务机器人的语音识别校准器。
职责：实时修正住客的语音识别结果，仅输出校准后的标准句子，不添加解释或多余字符。
规则：
数字：将口语数字转为阿拉伯数字，并统一“房间”为量词。
例：
输入：请带我去三号防线 → 输出：请带我去3号房间
常见误识别：自动替换易错词（如“适度”→“湿度”）。
例：
输入：现在的适度怎么样 → 输出：现在的湿度怎么样
若句子无误，原样返回。""")


class CalibratorGPT:
    def __init__(self, ip=ip):
        self.system_content = GPT_role  
        self.url = f"http://{ip}:8080/rkllm_chat"
        print('<-CalibratorGPT Working...->')

    def contact(self, user_msg: str):
        start_time = time()
        messages = [{"role":"system", "content":self.system_content}]
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
            print(f"<-LocalGPT used time: {time()-start_time:.2f}s->")
            return ""
        print(f"<-LocalGPT used time: {time()-start_time:.2f}s->")
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
    C = CalibratorGPT("127.0.0.1")
    while True:
        question = input('我:')
        if question:
            print(C.contact(question))