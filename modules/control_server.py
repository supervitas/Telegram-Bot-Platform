# -*- coding: utf-8 -*-
__author__ = 'nikolaev'
import subprocess as sub
import threading
import main_handler


pid = 0


def handler(message, user_id):
        global pid
        message = message.split(" ")
        if message == 'break':
            sub.Popen(("kill", str(pid)))

        try:
                process = sub.Popen(message, stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE)
                pid = process.pid
                for row in process.stdout:
                    main_handler.Respond.send_text_respond(row, user_id)
                for row in process.stderr:
                    main_handler.Respond.send_text_respond(row, user_id)
        except Exception:
                 main_handler.Respond.send_text_respond("Не правильная комманда",user_id)
