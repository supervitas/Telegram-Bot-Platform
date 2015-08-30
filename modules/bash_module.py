__author__ = 'nikolaev'
import subprocess as sub
from main_handler import Respond

def handler(message, user_id):

        process = sub.Popen('/Users/nikolaev/flud.sh', stdout=sub.PIPE, stderr=sub.PIPE)
        for row in process.stdout:
            Respond.send_text_respond(row, user_id)