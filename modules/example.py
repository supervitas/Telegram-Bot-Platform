# -*- coding: utf-8 -*-
__author__ = 'nikolaev'
import main_handler


def handler(message, user_id):  # функция которая принимает сообщение от главного модуля(Должна быть реализована обязательно)

    main_handler.Respond.send_text_respond(message, user_id)  # отправляем обратно