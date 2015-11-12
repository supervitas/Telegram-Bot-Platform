# -*- coding: utf-8 -*-
__author__ = 'nikolaev'
from main_handler import Respond  # Подключаем только класс ответа на сообщения


def handler(message, user_id):  # функция которая принимает сообщение от главного модуля(Должна быть реализована обязательно)

    Respond.send_text_respond(message, user_id)  # отправляем обратно