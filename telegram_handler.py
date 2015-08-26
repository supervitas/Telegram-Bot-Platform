__author__ = 'nikolaev'
# -*- coding: utf-8 -*-
import requests


INTERVAL = 5  # Интервал проверки наличия новых сообщений (обновлений) на сервере в секундах
ADMIN_ID = 54052993  # ID пользователя. Комманды от других пользователей выполняться не будут
TEMP_ID = 0
flag = 0
URL = 'https://api.telegram.org/bot'  # Адрес HTTP Bot API
TOKEN = '94799839:AAEOHMOexXt-X-3tnMCPT2VzC1b63fTpo9c'  # Ключ авторизации для Вашего бота
offset = 0
current_time = 0
now_plus_10 = 0
pid = 0


def make_url_query_string(params):
    return '?' + '&'.join([str(key) + '=' + str(params[key]) for key in params])


def check_updates(limit=5):

    global offset, TEMP_ID, pid
    params = make_url_query_string({'offset': offset+1, 'limit': limit, 'timeout': 0})
    request = requests.get(URL + TOKEN + '/getUpdates' + params) # Отправка запроса обновлений

    if not request.status_code == 200: return False # Проверка ответа сервера
    if not request.json()['ok']: return False # Проверка успешности обращения к API
    if not request.json()['result']: return False # Проверка наличия обновлений в возвращенном списке

    for update in request.json()['result']: # Проверка каждого элемента списка
        offset = update['update_id'] # Извлечение ID сообщения
        from_id = update['message']['from']['id'] # Извлечение ID отправителя
        name = update['message']['from']['first_name']
        surname = update['message']['from']['last_name']
        message = update['message']['text']





