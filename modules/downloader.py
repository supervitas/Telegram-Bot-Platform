__author__ = 'nikolaev'

import os, sys
import subprocess as sub
from main_handler import Respond
import urllib

def handler(message, user_id):

    message = message.split(" ")

    if message[0] == 'send':
        try:
            Respond.send_document(user_id, os.path.dirname(sys.argv[0]) + '/Downloads/' + " ".join(message[1:]))
            return
        except Exception:
            Respond.send_text_respond('File not found', user_id)
            return

    if message[0] == 'ls':
        lists = sub.Popen(('ls', os.path.dirname(sys.argv[0]) + '/Downloads/'), stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE)
        for row in lists.stdout:
            Respond.send_text_respond(row, user_id)
        return

    try:
        path = message[0]
        name_of_file = os.path.dirname(sys.argv[0]) + '/Downloads/' + message[1]

        urllib.urlretrieve (path, name_of_file)

        Respond.send_text_respond("Downloaded", user_id)
    except Exception:
        Respond.send_text_respond("Usage - url filename")
