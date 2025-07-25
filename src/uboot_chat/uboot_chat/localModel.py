import sys
import requests
import json
import re
from queue import Queue
from time import time

# Set the address of the Server.
# server_url = 'http://192.168.0.106:8080/rkllm_chat'
ip = "127.0.0.1"
# Create a session object.
session = requests.Session()
session.keep_alive = False  # Close the connection pool to maintain a long connection.
adapter = requests.adapters.HTTPAdapter(max_retries=5)
session.mount('https://', adapter)
session.mount('http://', adapter)
    
# ----------------- 全局变量 -----------------
HISTORY_MAX = 0                # 上下文轮数

class History:
    def __init__(self, max_size=10):
        self.max_size = max_size
        self.contain = []

    def update(self, data):
        self.contain.append(data)
        if len(self.contain) > self.max_size:
            self.contain = self.contain[1:]

GPT_role = (
    "uboot征服者酒店服务机器人，提供：1)带路服务 2)环境查询"
    "规则："
    "- 去房间（如'到1001'）→调用func_getPos"
    "- 问现在的温度/湿度 →调用func_getStatus"
    "- 其他问题直接回答"
    "回应要求：口语化、简洁亲切，不解释机制"
)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "func_getPos",
            "description": "用户要去具体房间时触发，提取纯数字房间号（如'1001房'→1001）",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {"type": "integer", "description": "数字房间号"}
                },
                "required": ["number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "func_getStatus",
            "description": "用户查询现在的'温度'或'湿度'时触发，调用此函数查询。",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string", "enum": ["温度", "湿度"]}
                },
                "required": ["status"]
            }
        }
    },
]

# ----------------- 工具函数实现 -----------------
def func_getPos(number: int) -> str:
    return f"好的，这就去{number}号房间。"

def func_getStatus(status: str) -> str:
    if status == "温度":
        return ""
    elif status == "湿度":
        return ""
    return "暂不支持的状态查询"

def func_test(a: int, b: int) -> int:
    return a * b

# 工具路由表
tool_map = {
    "func_getPos": func_getPos,
    "func_getStatus": func_getStatus,
    "func_test": func_test,
}


class LocalGPT:
    def __init__(self, ip=ip):
        self.history = History(HISTORY_MAX)
        self.system_content = GPT_role  
        self.user_requirements = Queue()
        self.url = f"http://{ip}:8080/rkllm_chat"

        print('<-LocalGPT initing...->')
        self.contact("带我去3号房间")
        self.contact("现在温度怎么样")
        self.contact("现在湿度怎么样")
        print('<-LocalGPT Working...->')

    def contact(self, user_msg: str):
        start_time = time()
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
            "tools": TOOLS
        }
        try:
            # Send a POST request
            responses = session.post(self.url, json=data, headers=headers, stream=False, verify=False)
        except requests.exceptions.ConnectionError:
            print("<-Local Model: 主机已离线->")
            return ""
        print(f"<-LocalGPT used time: {time()-start_time:.2f}s->")
        # Parse the response
        if responses.status_code == 200:
            # print("Q:", data["messages"][-1]["content"], '\n')
            
            server_answer = json.loads(responses.text)["choices"][-1]["message"]["content"]
            matches = re.findall(r"<tool_call>\s*(\{.*?\})\s*</tool_call>", ''.join(server_answer), re.DOTALL)
            # print("server_answer:", server_answer, '\n')
            
            result = [json.loads(match) for match in matches]
            for function_call in result:
                messages.append({'role': 'assistant', 'content': '', 'function_call':function_call}) 

            tool_calls = [{'function': result[i]} for i in range(len(result))]
            function_call = []
            for tool_call in tool_calls:
                if fn_call := tool_call.get("function"):
                    fn_name: str = fn_call["name"]
                    fn_args: dict = fn_call["arguments"]
                    param = list(fn_call["arguments"].values())[0]
                    print(f"<-LocalGPT: Function Callback success ({fn_name}), arg:{param}->")
                    self.user_requirements.put(param)
                    fn_res: str = str(tool_map[fn_name](**fn_args))
                    # messages.append({'role': 'tool', 'name': fn_name, 'content':fn_res})
                    function_call.append({'name': fn_name, 'arguments': fn_args})
            if function_call:
                return fn_res
            return server_answer.replace("<tool_call>", "").replace("</tool_call>", "").strip()
            
        else:
            print("Error:", responses.text)
            return "网络连接错误，请重试"
    
    def end(self):
        print('<-LocalGPT END->')
        


if __name__ == '__main__':
    GPT = LocalGPT("127.0.0.1")
    while True:
        question = input('我:')
        if question:
            print(GPT.contact(question))
