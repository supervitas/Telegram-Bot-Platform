__author__ = 'nikolaev'

from main_handler import Respond


def handler (message, user_id):
    Respond.send_text_respond("Hi I am first module!Be free to change me - /ssh - controls "
                              "/downloader - download  files. Both modules can send your files usage - send filename", user_id )
