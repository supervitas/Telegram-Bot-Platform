__author__ = 'nikolaev'

from main_handler import Respond


def handler (message, user_id):
    Respond.send_text_respond("Hi!I am first module! Now you can change me use /ssh to try sending command to your server in telegram",user_id)
