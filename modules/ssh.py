# -*- coding: utf-8 -*-
__author__ = 'nikolaev'
import subprocess as sub
import threading
from main_handler import Respond


pid = 0


def handler(message, user_id):
        global pid
        message = message.split(" ")
        if message[0] == 'stop' and pid != 0:
            sub.Popen(("kill", str(pid)))
            return
        if message[0] == 'send':
            try:
                Respond.send_document(user_id, message[1])
            except Exception:
                Respond.send_text_respond('File not found', user_id)
        else:

            p1 = threading.Thread(target=process_worker, args=[message, user_id])
            p1.start()


def process_worker(message, user_id):
    global pid
    try:

        if (message[0] == 'ping'):
            message.insert(1, '-c')
            message.insert(2, '4')
        process = sub.Popen(message, stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE)
        pid = process.pid
        for row in process.stdout:
            Respond.send_text_respond(row, user_id)
        for row in process.stderr:
            Respond.send_text_respond(row, user_id)
    except Exception:
             Respond.send_text_respond("Не правильная комманда",user_id)
