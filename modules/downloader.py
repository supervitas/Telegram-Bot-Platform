__author__ = 'nikolaev'

<<<<<<< HEAD
import os, sys
import subprocess as sub
=======
import os
>>>>>>> 9aa84169a204817b739a78ef697a2c155c676571
from main_handler import Respond
import  subprocess as sub
import urllib

def handler(message, user_id):

    message = message.split(" ")

    if message[0] == 'send':
        try:
<<<<<<< HEAD
            Respond.send_document(user_id, os.path.dirname(sys.argv[0]) + '/Downloads/' + " ".join(message[1:]))
=======
            Respond.send_document(user_id, 'Downloads/' + " ".join(message[1:]))
>>>>>>> 9aa84169a204817b739a78ef697a2c155c676571
            return
        except Exception:
            Respond.send_text_respond('File not found', user_id)
            return

    if message[0] == 'ls':
<<<<<<< HEAD
        lists = sub.Popen(('ls', os.path.dirname(sys.argv[0]) + '/Downloads/'), stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE)
=======
        lists = sub.Popen(('ls', 'Downloads/'), stdout=sub.PIPE, stdin=sub.PIPE, stderr=sub.PIPE)
>>>>>>> 9aa84169a204817b739a78ef697a2c155c676571
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
