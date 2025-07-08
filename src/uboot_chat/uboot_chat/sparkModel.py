from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from sparkai.errors import SparkAIConnectionError
from sparkai.core.utils.function_calling import convert_to_openai_function
from queue import Queue

SPARKAI_URL = 'wss://spark-api.xf-yun.com/v4.0/chat'
SPARKAI_APP_ID = 'ce227ede'
SPARKAI_API_SECRET = 'OWU2YTVlYzdiYWE2MGNmMWQ2ZGZlOWY2'
SPARKAI_API_KEY = '3e61db5044ba85695db2fd3c7f03ab04'
SPARKAI_DOMAIN = '4.0Ultra'

contents_size = 2  # 上下文的最大数量
GPT_role = ("你是uboot征服者酒店的酒店服务机器人（酒店地址在深圳龙华）。在用户与你对话时你要注意对方的语调和情绪来回答，"
            "回答时不用给出具体的解析过程，并且你的回答必须精简且口语化。")


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
        print('<-SparkGPT Working...->')
        print('<-SparkGPT:{} ->'.format(self.contact('你好')))

    def contact(self, user_msg: str):
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
                    number = eval(answer.generations[0][0].message.function_call['arguments'])['number']
                    answer_text = self._call_server(number)
                elif function_name == 'func_getStatus':
                    status = eval(answer.generations[0][0].message.function_call['arguments'])['status']
                    answer_text = self._call_status(status)
            except SyntaxError:
                print('<-SparkGPT: 解析错误->')
                return '解析错误'
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
    def func_getPos(number: int) ->str:
        """你是一个房间位置查询器，当要去某号房间时，可以帮我查询该房间号对应的位置。例如：带我去3号房间，或带我去7号房间，或带我去9号房间，或带我去八号房间
    Args:
        number: 输入房间号
    Return:
             返回 房间的位置
    """
        return "位置"

    @staticmethod
    def func_getStatus(status: str) -> str:
        """你是一个'温度'和'湿度'查询器，可以帮我查询当前环境的温度或湿度。例如：现在的温度怎么样、现在多少度、房间的湿度怎么样
    Args:
        status: 输入'温度'或'湿度'
    Return:
             返回 房间内的状态
        """

    @staticmethod
    def func_test(a, b: int) -> int:
        """你是一个乘法计算器，可以帮我计算两个数的乘积，例如：计算1乘1等于几或计算1*1等于几
        Args:
            a: 输入a
            b: 输入b
        Return:
             返回 a*b 结果
        """
        print("hello success")
        return a * b


if __name__ == '__main__':
    from time import sleep
    sparkGPT = SparkGPT()
    sleep(0.5)
    print(sparkGPT.contact("带我去316房间"))
    sleep(0.5)
    # print(sparkGPT.contact("现在温度怎么样"))
    while True:
        question = input('我:')
        if question:
            print(sparkGPT.contact(question))
