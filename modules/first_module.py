__author__ = 'nikolaev'

import glob
import os
from main_handler import Respond

path = os.path.dirname(os.path.abspath(__file__))
print path
print glob.glob(path)



def handler (message, user_id):
    Respond.send_text_respond("Hi I am first module!My current modules are %s " %modules, user_id )
