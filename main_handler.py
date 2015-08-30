# -*- coding: utf-8 -*-
__author__ = 'nikolaev'

import os
from datetime import datetime, timedelta
import requests
import settings
import threading
import modules

settings.check_config()
offset = 0
TEMP_ID = 0  # Временный ID админа.Присваивается отправлением пароля
URL = 'https://api.telegram.org/bot'  # Адрес HTTP Bot API
current_time = 0
now_plus_10 = 0
CURRENT_MODULE = 0
TOKEN = settings.load_config("GET_TOKEN")
ADMIN_ID = settings.load_config("GET_ADMIN_ID")
PASSWORD = settings.load_config("GET_PASSWORD")

def check_updates():

    global offset, CURRENT_MODULE

    data = {'offset': offset + 1, 'limit': 5, 'timeout': 0}  # Формируем параметры запроса
    request = requests.post(URL + TOKEN + '/getUpdates', data=data) # Отправка запроса обновлений

    if not request.status_code == 200: return False # Проверка ответа сервера
    if not request.json()['ok']: return False  # Проверка успешности обращения к API
    if not request.json()['result']: return False  # Проверка наличия обновлений в возвращенном списке

    for update in request.json()['result']: # Проверка каждого элемента списка
        offset = update['update_id']  # Извлечение ID сообщения
        from_id = update['message']['from']['id']  # Извлечение ID отправителя
        name = update['message']['from']['first_name']  # Извлечение имени
        surname = update['message']['from']['last_name']  # Извлечение фамилии
        message = update['message']['text']  # Извлечение сообщения

        message_thread= threading.Thread(target=message_distribution, args=[message,from_id,name,surname])
        message_thread.start()


def message_distribution(message, from_id, name, surname):  # Решает кому,что и куда отправлять
        global CURRENT_MODULE

        if (ADMIN_ID != from_id) and (message == settings.load_config("GET_PASSWORD")):
            Auth.login(from_id)
            Respond.send_text_respond("Auth Granted!", from_id)
            return

        if (ADMIN_ID == from_id) or (from_id == TEMP_ID and Auth.zero_access()):
            if (message[0] == "/"):
                CURRENT_MODULE = message[1::]
                return
            try:
                exec (('modules.%s.handler(message,from_id)')%CURRENT_MODULE)
                Logger.log_auth_user(message, from_id, name, surname)
            except Exception:
                Respond.send_text_respond("Module with this name not found", from_id)

        if (ADMIN_ID != from_id) and (from_id != TEMP_ID):
            Respond.send_text_respond("You are not autherised,%s.Please,enter password!"%name, from_id )
            Logger.log_notauth_user(message, from_id, name, surname)


class Respond:  # Класс отправления ответа
    @staticmethod
    def send_text_respond(text, chat_id):

        data = {'chat_id': chat_id, 'text': text}

        request = requests.post(URL + TOKEN + '/sendMessage', data=data)  # HTTP запрос
        if not request.status_code == 200: return False  # Проверка ответа сервера
        if not request.json()['ok']: return False  # Проверка успешности обращения к API
        return True

    @staticmethod
    def send_photo_respond(chat_id, name_of_photo):  # Метод отправки фото

        data = {'chat_id': chat_id}
        photo = {'photo': open(name_of_photo, 'rb')}

        request = requests.post(URL+TOKEN+'/sendPhoto', data=data, files=photo)

        if not request.status_code == 200: return False  # Проверка ответа сервера
        if not request.json()['ok']: return False  # Проверка успешности обращения к API
        return True

    @staticmethod
    def send_document(chat_id, name_of_file):  # Метод отправки файлов

        data = {'chat_id': chat_id}
        document = {'document': open(name_of_file, 'rb')}

        request = requests.post(URL+TOKEN+'/sendDocument', data=data, files=document)

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


class Logger:  # Класс отвечает за логирование + настройки

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
            f1.close(), f2.close()

if __name__ == '__main__':
    Logger.check_files()
    while True:
        try:
            check_updates()
        except KeyboardInterrupt:
            print "Stopped by user"
            break
        except KeyError:
            continue
