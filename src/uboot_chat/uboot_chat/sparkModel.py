from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from sparkai.errors import SparkAIConnectionError

SPARKAI_URL = 'wss://spark-api.xf-yun.com/v4.0/chat'
SPARKAI_APP_ID = 'ce227ede'
SPARKAI_API_SECRET = 'OWU2YTVlYzdiYWE2MGNmMWQ2ZGZlOWY2'
SPARKAI_API_KEY = '3e61db5044ba85695db2fd3c7f03ab04'
SPARKAI_DOMAIN = '4.0Ultra'

contents_size = 2  # 上下文的最大数量
GPT_role = ("你是uboot征服者酒店的酒店服务机器人（酒店地址在深圳龙华），在用户与你对话时你要注意对方的语调和情绪来回答，"
            "回答必须口语化，不用给出具体的解析过程，并在在回答之前，精简你的所有回答成一段简短的话。")


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
        self.user_requirements = []
        print('<-SparkGPT Working...->')

    def contact(self, user_msg: str):
        messages = [ChatMessage(role="system", content=self.system_content)]
        for msg in self.history.contain:
            messages.append(msg)
        user_chatMessage = ChatMessage(role="user", content=user_msg)
        messages.append(user_chatMessage)
        try:
            answer = self._spark.generate([messages], callbacks=[self.handler])  # , function_definition=self.function_definition)
            answer_text = answer.generations[0][0].text
        except SparkAIConnectionError:
            answer = ""
        # print(answer)
        if answer_text == "":
            answer_text = self._call_server(user_msg)
        self.history.update(user_chatMessage)
        self.history.update(ChatMessage(role="assistant", content=answer_text))
        return answer_text

    def _call_server(self, msg):
        self.user_requirements.append(msg)
        return '正在联系服务员...'

    def end(self):
        print('<-SparkGPT END->')


if __name__ == '__main__':
    sparkGPT = SparkGPT()
    while True:
        question = input('我:')
        if question:
            print(sparkGPT.contact(question))
