# -*- coding: utf-8 -*-
__author__ = 'nikolaev'

import control_server, settings
import requests
import os
from datetime import datetime, timedelta

offset = 0
TEMP_ID = 0  # Временный ID админа.Присваивается отправлением пароля
TEMP_PASSWORD = 0
URL = 'https://api.telegram.org/bot'  # Адрес HTTP Bot API
current_time = 0
now_plus_10 = 0
TOKEN = settings.load_config("GET_TOKEN")
ADMIN_ID = settings.load_config("GET_ADMIN_ID")

def make_url_query_string(params):
    return '?' + '&'.join([str(key) + '=' + str(params[key]) for key in params])


def check_updates(limit=5):

    global offset

    params = make_url_query_string({'offset': offset+1, 'limit': limit, 'timeout': 0})
    request = requests.get(URL + TOKEN + '/getUpdates' + params) # Отправка запроса обновлений

    if not request.status_code == 200: return False # Проверка ответа сервера
    if not request.json()['ok']: return False # Проверка успешности обращения к API
    if not request.json()['result']: return False # Проверка наличия обновлений в возвращенном списке

    for update in request.json()['result']: # Проверка каждого элемента списка
        offset = update['update_id']  # Извлечение ID сообщения
        from_id = update['message']['from']['id']  # Извлечение ID отправителя
        name = update['message']['from']['first_name']
        surname = update['message']['from']['last_name']
        message = update['message']['text']

        if (ADMIN_ID == from_id) or (from_id == TEMP_ID and Auth.zero_access()):
            Logger.log_auth_user(message, from_id, name, surname)
            control_server.current_command(message, from_id)

        if (ADMIN_ID != from_id) and (from_id != TEMP_ID):
            Logger.log_notauth_user(message, from_id, name, surname)


class Respond:  # Класс отправления ответа
    @staticmethod
    def send_text_respond(text, chat_id):
        TOKEN = settings.load_config("GET_TOKEN")
        params = make_url_query_string({'chat_id': chat_id, 'text': text}) # Преобразование параметров
        request = requests.get(URL + TOKEN + '/sendMessage' + params) # HTTP запрос
        if not request.status_code == 200: return False  # Проверка ответа сервера
        if not request.json()['ok']: return False  # Проверка успешности обращения к API
        return True


class Auth:  # Класс авторизации
    @staticmethod
    def login(id): # Функция авторизации длится 10 минут
        global TEMP_ID, current_time, now_plus_10
        TEMP_ID = id
        current_time = datetime.now()
        now_plus_10 = current_time + timedelta(minutes=10)

    @staticmethod
    def zero_access():  # Проверка истечения админки
        global current_time, now_plus_10, TEMP_ID
        if (datetime.now() < now_plus_10):
            return True
        else:
            TEMP_ID = 0
            return False


class Logger:  # Класс отвечает за создание лог файлов, и логирование

    @staticmethod
    def log_notauth_user(message, from_id, name, surname):
        f = open('logs/not_auth_msg.log', 'a')
        f.write("Message - %s    id - %s Name - %s %s " %(message, from_id, name, surname) + "  %s" % datetime.now() + '\n')

    @staticmethod
    def log_auth_user(message, from_id, name, surname):
        f = open('logs/auth_msg.log', 'a')
        f.write("Message - %s    id - %s Name - %s %s " %(message, from_id, name, surname) + "  %s" % datetime.now() + '\n')

    @staticmethod
    def check_files():  # Создаем файлы логов и настроек
        if not (os.path.isfile('logs/auth_msg.log') and os.path.isfile('logs/not_auth_msg.log')):
            if not (os.path.isdir('logs')):
                os.mkdir('logs')
            f1 = open('logs/not_auth_msg.log', 'w')
            f2 = open('logs/auth_msg.log', 'w')
            f1.close()
            f2.close()
        settings.check_config()


if __name__ == '__main__':
    Logger.check_files()
    while True:
        check_updates(1)

