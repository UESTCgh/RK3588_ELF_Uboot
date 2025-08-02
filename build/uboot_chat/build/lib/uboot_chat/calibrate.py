from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from time import time


SPARKAI_URL = 'wss://spark-api.xf-yun.com/v4.0/chat'
SPARKAI_APP_ID = 'ce227ede'
SPARKAI_API_SECRET = 'OWU2YTVlYzdiYWE2MGNmMWQ2ZGZlOWY2'
SPARKAI_API_KEY = '3e61db5044ba85695db2fd3c7f03ab04'
SPARKAI_DOMAIN = '4.0Ultra'

contents_size = 2  # 上下文的最大数量
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
    def __init__(self, role = GPT_role):
        self.history = History(contents_size)
        self._spark = ChatSparkLLM(spark_api_url=SPARKAI_URL,
                                   spark_app_id=SPARKAI_APP_ID,
                                   spark_api_key=SPARKAI_API_KEY,
                                   spark_api_secret=SPARKAI_API_SECRET,
                                   spark_llm_domain=SPARKAI_DOMAIN,
                                   streaming=False,
                                   )
        self.system_content = role
        self.handler = ChunkPrintHandler()
        self.history.update(ChatMessage(role="user", content="请带我去三号防线"))
        self.history.update(ChatMessage(role="assistant", content="请带我去3号房间"))
        print('<-CalibratorGPT Working...->')

    def contact(self, user_msg: str):
        start_time = time()
        messages = [ChatMessage(role="system", content=self.system_content)]
        for msg in self.history.contain:
            messages.append(msg)
        user_chatMessage = ChatMessage(role="user", content=user_msg)
        messages.append(user_chatMessage)
        answer = self._spark.generate([messages], callbacks=[self.handler])  # , function_definition=self.function_definition)
        # print(answer)
        answer_text = answer.generations[0][0].text
        if answer_text == "":
            answer_text = self._call_server()
        print(f'<-CalibratorGPT used time {time()-start_time:.2f}s->')
        return answer_text

    @staticmethod
    def _call_server():
        return '你好'

    def end(self):
        print('<-CalibratorGPT END->')


if __name__ == "__main__":
    C = CalibratorGPT()
    while True:
        question = input('我:')
        if question:
            print(C.contact(question))