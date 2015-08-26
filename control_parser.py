# -*- coding: utf-8 -*-
__author__ = 'nikolaev'
import requests
import os
import time
import subprocess as sub
import threading
from datetime import datetime, timedelta

INTERVAL = 5 # Интервал проверки наличия новых сообщений (обновлений) на сервере в секундах
ADMIN_ID = 54052993 # ID пользователя. Комманды от других пользователей выполняться не будут
TEMP_ID = 0
flag=0
URL = 'https://api.telegram.org/bot' # Адрес HTTP Bot API
TOKEN = '94799839:AAEOHMOexXt-X-3tnMCPT2VzC1b63fTpo9c' # Ключ авторизации для Вашего бота
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

        if(ADMIN_ID == from_id) or (from_id == TEMP_ID and zero_access()):
            if (message == "break" and pid != 0):
                sub.Popen(("kill", str(pid)))
                break
            p1 = threading.Thread(target = message_confirmed, args = [message,from_id,name,surname])
            p1.start()
            break
        if (message == "password"):
            login(from_id)
            send_respond("Auth Granted!", from_id )
            break
        else:
            f = open('not_auth_msg.log', 'a')
            f.write("Message - %s    id - %s Name - %s %s " %(message,from_id,name ,surname) + "  %s" %datetime.now() + '\n')
            message = message.split(" ")
            f.close()
            send_respond("You are not autherised,%s.Please,enter password!"%name, from_id )


def message_confirmed(message, id, name, surname):

        f = open('auth_msg.log', 'a')
        f.write("Message - %s  id - %s Name - %s %s " %(message, id, name, surname) + "  %s" % datetime.now() + '\n')
        f.close()
        message = message.split(" ")
        t = threading.Thread(target=start_process(message, id))
        t.run()


def start_process(message,id):

        global pid
        try:
                process = sub.Popen((message), stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE)
                pid = process.pid
                for row in process.stdout:
                    send_respond(row,id)
                for row in process.stderr:
                    send_respond(row,id)
        except Exception:
                send_respond("Не правильная комманда",id)


def send_respond(text, chat_id):
    params = make_url_query_string({'chat_id': chat_id, 'text': text}) # Преобразование параметров
    request = requests.get(URL + TOKEN + '/sendMessage' + params) # HTTP запрос
    if not request.status_code == 200: return False # Проверка ответа сервера
    if not request.json()['ok']: return False # Проверка успешности обращения к API
    return True


def login(id):
    global TEMP_ID, curent_time, now_plus_10
    TEMP_ID = id
    curent_time = datetime.now()
    now_plus_10 = curent_time + timedelta(minutes=10)


def create_files():
    if not (os.path.isfile('auth_msg.log') and os.path.isfile('not_auth_msg.log')):
        f1 = open('not_auth_msg.log', 'w')
        f2 = open('auth_msg.log', 'w')
        f1.close()
        f2.close()


def zero_access():
    global current_time, now_plus_10, TEMP_ID
    if (datetime.now() < now_plus_10):
        return True
    else:
        TEMP_ID = 0
        return False


create_files()

while True:
    try:
        check_updates()
        time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print 'Прервано пользователем..'
        break
    except requests.exceptions.ConnectionError:
        time.sleep(10)
        continue
    except Exception:
        continue