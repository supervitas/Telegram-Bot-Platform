# -*- coding: utf-8 -*-
__author__ = 'nikolaev'
import subprocess as sub
import threading
import main_handler as handler


pid = 0


def main_handler(message, user_id):

        message = message.split(" ")
        t = threading.Thread(target=start_process(message, user_id))
        t.run()


def start_process(message, user_id):

        global pid
        try:
                process = sub.Popen(message, stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE)
                pid = process.pid
                for row in process.stdout:
                    handler.Respond.send_text_respond(row, user_id)
                for row in process.stderr:
                    handler.Respond.send_text_respond(row, user_id)
        except Exception:
                 handler.Respond.send_text_respond("Не правильная комманда",user_id)