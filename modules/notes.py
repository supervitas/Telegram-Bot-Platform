# -*- coding: utf-8 -*-
__author__ = 'nikolaev'
import os
from main_handler import Respond


def handler(message, user_id):
    check_file()
    if (message == 'print'):
        f1 = open('notes.txt', 'r')
        for row in f1:
            Respond.send_text_respond(row, user_id)
        return
    if (message == 'delete'):
        os.remove('notes.txt')
        Respond.send_text_respond('Note removed', user_id)
        return
    f1 = open('notes.txt', 'a')
    f1.write(message)
    f1.write('\n END OF NOTE \n')

    Respond.send_text_respond('Note saved :)', user_id)


def check_file():
    if not (os.path.isfile('notes.txt')):
        f1 = open('notes.txt', 'w')
        f1.close()
