__author__ = 'nikolaev'
from main_handler import Respond
import urllib

def handler(message, user_id):
    message = message.split(" ")

    if message[0] == 'send':
        try:
            Respond.send_document(user_id, message[1])
            return
        except Exception:
            Respond.send_text_respond('File not found', user_id)
            return

    try:

        path = message[0]
        name_of_file = message[1]

        urllib.urlretrieve (path, name_of_file)

        Respond.send_text_respond("Downloaded", user_id)
    except Exception:
        Respond.send_text_respond("Usage - url filename")
