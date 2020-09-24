import requests
import json


class Dora_client():
    def __init__(self):
        self.key = 'Your partner key'
        self.service = 'http://otherwave.ru/dora'

    def answer(self, quest):
        form = f'?&text={quest}&key={self.key}'
        response = requests.get(self.service + form)
        answer = json.loads(response.content)
        return answer

    def learn(self, quest, answer, author):
        form = f'?&quest={quest}&answer={answer}&author={author}&key={self.key}'
        response = requests.get(self.service + form)
        answer = json.loads(response.content)
        print(answer)
        return answer

    def rating(self, operator, response_id):
        form = f'?&operator={operator}&response_id={response_id}&key={self.key}'
        response = requests.get(self.service + form)
        answer = json.loads(response.content)
        return answer
