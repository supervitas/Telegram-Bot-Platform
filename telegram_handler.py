# -*- coding: utf-8 -*-
__author__ = 'nikolaev'

import requests
import os
from datetime import datetime, timedelta


INTERVAL = 5  # Интервал проверки наличия новых сообщений (обновлений) на сервере в секундах
ADMIN_ID = 54052993  # ID пользователя. Комманды от других пользователей выполняться не будут
TEMP_ID = 0  # Временный ID админа. Нужен в случае,если потребуется выполнять комманды не со своего аккаунта в телеграме
             # Присваивается отправлением пароля
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



def login(id): # Функция авторизации длится 10 минут
    global TEMP_ID, curent_time, now_plus_10
    TEMP_ID = id
    curent_time = datetime.now()
    now_plus_10 = curent_time + timedelta(minutes=10)


def zero_access(): # Проверка истечения админки
    global current_time, now_plus_10, TEMP_ID
    if (datetime.now() < now_plus_10):
        return True
    else:
        TEMP_ID = 0
        return False


class Logger:  # Класс отвечает за создание лог файлов, и логирование
    def __init__(self):
        pass

    @staticmethod
    def log_notauth_user(self,message,from_id,name,surname):
        f = open('not_auth_msg.log', 'a')
        f.write("Message - %s    id - %s Name - %s %s " %(message, from_id, name, surname) + "  %s" % datetime.now() + '\n')

    @staticmethod
    def log_auth_user(self,message,from_id,name,surname):
        f = open('auth_msg.log', 'a')
        f.write("Message - %s    id - %s Name - %s %s " %(message, from_id, name, surname) + "  %s" % datetime.now() + '\n')

    @staticmethod
    def create_files(self): # Создаем файлы логов
        if not (os.path.isfile('auth_msg.log') and os.path.isfile('not_auth_msg.log')):
            f1 = open('not_auth_msg.log', 'w')
            f2 = open('auth_msg.log', 'w')
            f1.close()
            f2.close()



while True:

    check_updates(1)



