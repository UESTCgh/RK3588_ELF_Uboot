from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from sparkai.errors import SparkAIConnectionError
from sparkai.core.utils.function_calling import convert_to_openai_function
from queue import Queue
from time import time, sleep
import re

SPARKAI_URL = 'wss://spark-api.xf-yun.com/v4.0/chat'
SPARKAI_APP_ID = 'ce227ede'
SPARKAI_API_SECRET = 'OWU2YTVlYzdiYWE2MGNmMWQ2ZGZlOWY2'
SPARKAI_API_KEY = '3e61db5044ba85695db2fd3c7f03ab04'
SPARKAI_DOMAIN = '4.0Ultra'

contents_size = 2  # 上下文的最大数量
GPT_role = (
    "你是uboot征服者酒店(深圳龙华)的服务机器人，严格遵守以下指令：\n"
    "1. 函数调用优先级高于直接回答\n"
    "2. 当用户表达位置需求时，必须调用func_getPos\n"
    "   - 触发词：去/到/带我去/房间/楼层/号房\n"
    "   - 示例：'去1001'/'带我到三楼'/'请送我去八号房间'\n"
    "   - 自动转换：中文数字转阿拉伯数字（'三楼'→3，'八号'→8）\n"
    "3. 当询问环境参数时，必须调用func_getStatus\n"
    "   - 温度相关：热/冷/温度/多少度\n"
    "   - 湿度相关：湿度/潮湿/闷\n"
    "4. 其他问题直接回答\n\n"
)


class History:
    def __init__(self, max_size=10):
        self.max_size = max_size
        self.contain = []

    def update(self, data):
        self.contain.append(data)
        if len(self.contain) > self.max_size:
            self.contain = self.contain[1:]


class SparkGPT:
    def __init__(self):
        self.history = History(contents_size)
        self._spark = ChatSparkLLM(spark_api_url=SPARKAI_URL,
                                   spark_app_id=SPARKAI_APP_ID,
                                   spark_api_key=SPARKAI_API_KEY,
                                   spark_api_secret=SPARKAI_API_SECRET,
                                   spark_llm_domain=SPARKAI_DOMAIN,
                                   streaming=False,
                                   )
        self.system_content = GPT_role
        self.handler = ChunkPrintHandler()
        self.user_requirements = Queue()
        self.function_definition = [convert_to_openai_function(self.func_getPos), convert_to_openai_function(self.func_getStatus)]
        print('<-sparkGPT initing...->')
        self.contact("带我去3号房间")
        sleep(0.2)
        self.contact("现在温度怎么样")
        sleep(0.2)
        self.contact("现在湿度怎么样")
        sleep(0.2)
        print('<-SparkGPT Working...->')
        print('<-SparkGPT:{} ->'.format(self.contact('你好')))

    def contact(self, user_msg: str):
        start_time = time()
        messages = [ChatMessage(role="system", content=self.system_content)]
        for msg in self.history.contain:
            messages.append(msg)
        user_chatMessage = ChatMessage(role="user", content=user_msg)
        messages.append(user_chatMessage)
        try:
            answer = self._spark.generate([messages], callbacks=[self.handler], function_definition=self.function_definition)
            # print(answer)
            answer_text = answer.generations[0][0].text
        except SparkAIConnectionError:
            print("<-SparkGPT: 网络连接错误，请重试->")
            return "网络连接错误，请重试"
        except IndexError:
            print("<-SparkGPT: 服务端返回错误，请重试->")
            return "服务端返回错误，请重试"
        # print(answer)
        if answer_text == "":
            try:
                function_name = answer.generations[0][0].message.function_call['name']
                print(f"<-SparkGPT: Function Callback success ({function_name})->")
                if function_name == 'func_getPos':
                    # number = eval(answer.generations[0][0].message.function_call['arguments'])['number']
                    match = re.search(r"(?:去|到|带我去|送我去)?\s*(\d{1,4})\s*(?:号房|房间|房)?", user_msg)
                    number = int(match.group(1))
                    answer_text = self._call_server(number)
                elif function_name == 'func_getStatus':
                    # status = eval(answer.generations[0][0].message.function_call['arguments'])['status']
                    if re.search(r"温度", user_msg):
                        status = "温度"
                    else:
                        status = "湿度"
                    answer_text = self._call_status(status)
            except SyntaxError:
                print('<-SparkGPT: 解析错误->')
                return '解析错误'
        print(f"<-sparkGPT used time: {time()-start_time:.2f}s->")
        self.history.update(user_chatMessage)
        if answer_text:
            self.history.update(ChatMessage(role="assistant", content=answer_text))
        return answer_text

    def _call_server(self, msg):
        self.user_requirements.put(msg)
        return f'好的，这就去{msg}号房间'
    
    def _call_status(self, status):
        self.user_requirements.put(status)
        return ''

    def end(self):
        print('<-SparkGPT END->')

    @staticmethod
    def func_getPos(number: int) -> str:
        """
        房间位置查询函数（触发条件：含'房间''带我去''位置'等关键词+3-4位数字）
        Args:
            number: 输入房间号
        Return:
                房间的位置

        """

    @staticmethod
    def func_getStatus(status: str) -> str:
        """严格处理环境查询：当且仅当包含温度/湿度关键词时调用
        Args:
            status: 映射用户输入到指定值（
                    示例：'热吗'→温度, '潮湿'→湿度）
        Return:
            返回环境状态数据
        """


if __name__ == '__main__':
    from time import sleep
    sparkGPT = SparkGPT()
    # print(sparkGPT.contact("现在温度怎么样"))
    while True:
        question = input('我:')
        if question:
            print(sparkGPT.contact(question))

        """
        match = re.search(r"(?:去|到|带我去|送我去)?\s*(\d{1,4})\s*(?:号房|房间|房)?", user_msg)
        if match:
            number = int(match.group(1))
            self.user_requirements.put(number)
            print(f"<-LocalGPT: Function Callback success (func_getPos)->")
            return func_getPos(number)
        if re.search(r"温度", user_msg):
            self.user_requirements.put("温度")
            print(f"<-LocalGPT: Function Callback success (func_getStatus)->")
            return ""
        if re.search(r"湿度", user_msg):
            self.user_requirements.put("湿度")
            print(f"<-LocalGPT: Function Callback success (func_getStatus)->")
            return ""
        """