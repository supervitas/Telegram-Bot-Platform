# -*- coding: utf-8 -*-
__author__ = 'nikolaev'

import os,sys
from time import sleep, gmtime, strftime
from datetime import datetime, timedelta
import requests
import settings
import threading
import urllib
import modules


settings.check_config()
offset = 0
TEMP_ID = 0  # Временный ID админа.Присваивается отправлением пароля
URL = 'https://api.telegram.org/bot'  # Адрес HTTP Bot API
current_time = 0
now_plus_10 = 0
CURRENT_MODULE = 'first_module'
TOKEN = settings.load_config("GET_TOKEN")
ADMIN_ID = settings.load_config("GET_ADMIN_ID")
PASSWORD = settings.load_config("GET_PASSWORD")


class Handler:
    def __init__(self, TOKEN = settings.load_config("GET_TOKEN"),
                 ADMIN_ID = settings.load_config("GET_ADMIN_ID"),
                 PASSWORD = settings.load_config("GET_PASSWORD"),
                 CURRENT_MODULE = 'ssh'):
        self.current_module = CURRENT_MODULE
        self.offset = 0
        self.token = TOKEN
        self.password = PASSWORD
        self.admin_id = ADMIN_ID
        self.temp_id = TEMP_ID
        self.current_time = 0
        self.now_plus_10 = 0

    def check_updates(self):  # Проверяет обновления

        data = {'offset': self.offset + 1, 'limit': 5, 'timeout': 0}  # Формируем параметры запроса
        request = requests.get(URL + TOKEN + '/getUpdates', data=data)  # Отправка запроса обновлений


        if not request.status_code == 200: return False # Проверка ответа сервера
        if not request.json()['ok']: return False  # Проверка успешности обращения к API
        if not request.json()['result']: return False  # Проверка наличия обновлений в возвращенном списке
        for update in request.json()['result']: # Проверка каждого элемента списка
            self.offset = update['update_id']  # Извлечение ID сообщения

            photo_id = 0
            file_id = 0
            message = ' '
            file_name = 0

            mes = update['message']
            if ('document' in mes):
                file_id = update['message']['document']['file_id']  # Извлечение контента
                file_name = update['message']['document']['file_name']
            if ('photo' in mes):
                photo_id = update['message']['photo'][0]['file_id']

            from_id = update['message']['from']['id']  # Извлечение ID отправителя
            name = update['message']['from']['first_name']  # Извлечение имени
            surname = update['message']['from']['last_name']  # Извлечение фамилии
            if ('text' in mes):
                message = update['message']['text']  # Извлечение сообщения

            message_thread = threading.Thread(target=self.message_distribution, args=[message, from_id, name, surname, file_id, file_name, photo_id])
            message_thread.start()

    def message_distribution(self, message, from_id, name, surname, file_id, file_name, photo_id):  # Решает кому,что и куда отправлять

            if (self.admin_id != from_id) and (message == self.password):
                self.login(from_id)
                Respond.send_text_respond("Auth Granted!", from_id)
                return

            if (self.admin_id == from_id) or (from_id == self.temp_id and self.zero_access()):

                if (file_id != 0):
                    Respond.getFile(file_id, file_name)
                    Respond.send_text_respond('Download complete!:)', from_id)
                    return
                if (photo_id !=0 ):
                    Respond.getFile(photo_id)
                    Respond.send_text_respond('Downloaded:)', from_id)
                    return

                if (message[0] == "/"):
                    self.current_module = message[1::]
                    return
                try:
                    exec (('modules.%s.handler(message,from_id)')% self.current_module)
                    Logger.log_auth_user(message, from_id, name, surname)
                except Exception:
                    Respond.send_text_respond("Some Error", from_id)

            if (self.admin_id != from_id) and (from_id != self.temp_id):
                Respond.send_text_respond("You are not autherised,%s.Please,enter password!"%name, from_id )
                Logger.log_notauth_user(message, from_id, name, surname)

    def login(self, id):  # Функция авторизации длится 10 минут
        self.temp_id = id
        self.current_time = datetime.now()
        self.now_plus_10 = self.current_time + timedelta(minutes=10)

    def zero_access(self):  # Проверка истечения админки
        if (self.datetime.now() < self.now_plus_10):
            return True
        else:
            self.temp_id = 0
            return False


class Respond:  # Класс ответов
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


    @staticmethod
    def getFile(file_id, file_name=strftime("%a, %d %b %Y %H:%M:%S.jpg", gmtime())):
        data = {'file_id': file_id}  # Формируем параметры запроса
        request = requests.get(URL + TOKEN + '/getFile', data=data)  # Отправка запроса обновлений
        path = 'https://api.telegram.org/file/bot'+TOKEN+'/'+request.json()['result']['file_path']
        pathname = os.path.dirname(sys.argv[0])
        name_of_file = pathname + '/Downloads/' + file_name
        urllib.urlretrieve (path, name_of_file)


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
        if not (os.path.isdir('Downloads')):
            os.mkdir('Downloads')
        if not (os.path.isfile('logs/auth_msg.log') and os.path.isfile('logs/not_auth_msg.log')):
            if not (os.path.isdir('logs')):
                os.mkdir('logs')
            f1 = open('logs/not_auth_msg.log', 'w')
            f2 = open('logs/auth_msg.log', 'w')
            f1.close(), f2.close()


if __name__ == '__main__':
    main_handler = Handler()
    Logger.check_files()

    while True:
        try:
            main_handler.check_updates()
            sleep(2)
        except KeyboardInterrupt:
            print "Stopped by user"
            break

        except KeyError:
            continue
