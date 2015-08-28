# -*- coding: utf-8 -*-
__author__ = 'nikolaev'

import ConfigParser
import os


def make_config():
    admin_id = raw_input("Enter admin id in telegram:")
    token = raw_input("Enter token for your bot:")
    admin_password = raw_input("Enter password for access your bot not only with your device:")

    parser = ConfigParser.RawConfigParser()

    parser.add_section('Main Settings')

    parser.set('Main Settings', 'admin_id', admin_id)
    parser.set('Main Settings', 'Token', token)
    parser.set('Main Settings', 'Admin password', admin_password)

    config_file = open('telegram_settings.conf', "wb")
    parser.write(config_file)
    config_file.close()


def load_config(case):
    parser = ConfigParser.SafeConfigParser()
    parser.read('telegram_settings.conf')

    ADMIN_ID = int(parser.get('Main Settings', 'admin_id'))
    TOKEN = parser.get('Main Settings', 'token')
    TEMP_PASSWORD = parser.get('Main Settings', 'admin password')

    if (case == 'GET_ADMIN_ID'):
        return ADMIN_ID
    elif (case == 'GET_TOKEN'):
        return TOKEN
    else:
        return TEMP_PASSWORD


def check_config():
    if not (os.path.isfile('telegram_settings.conf')):
        make_config()
