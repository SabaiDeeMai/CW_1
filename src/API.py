import requests


url_get = "https://httpbin.org/get" # используемый адрес для отправки запроса

response = requests.get(url_get) # отправка GET-запроса

print(response) # вывод объекта класса Response
# Вывод:
# >> <Response [200]>

print(response.status_code) # вывод статуса запроса, 200 означает, что всё хорошо, остальные коды нас пока не интересуют и их можно считать показателем ошибки
# Вывод:
# >> 200

print(response.text) # печать ответа в виде текста того, что вернул нам внешний сервис
# Вывод:
# >> {
# >>   "args": {},
# >>   "headers": {
# >>     "Accept": "*/*",
# >>     "Accept-Encoding": "gzip, deflate",
# >>     "Host": "httpbin.org",
# >>     "User-Agent": "python-requests/2.31.0",
# >>     "X-Amzn-Trace-Id": "Root=1-65892ff5-5f3e46891d0c56775f3dc659"
# >>   },
# >>   "origin": "185.252.41.5",
# >>   "url": "https://httpbin.org/get"
# >> }

print(response.json()) # печать ответа в виде json-объекта того, что нам вернул внешний сервис
# Вывод:
# >> {'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.31.0', 'X-Amzn-Trace-Id': 'Root=1-65892ff5-5f3e46891d0c56775f3dc659'}, 'origin': '185.252.41.5', 'url': 'https://httpbin.org/get'}


class HeadHunterAPI:
    def get_vacancies(self, param):
        pass
