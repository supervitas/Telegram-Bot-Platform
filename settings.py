__author__ = 'nikolaev'
import ConfigParser
import os

def make_config():
    admin_id = raw_input("Enter admin id in telegram:")
    token = raw_input("Enter token for your bot:")
    admin_password = raw_input("Enter password for access your bot not only with your device:")

    parser = ConfigParser.SafeConfigParser()
    config_file = open("telegram_settings.conf", "w")
    parser.add_section('Main Settings')

    parser.set('Main Settings', 'admin_id', admin_id)
    parser.set('Main Settings', 'Token', token)
    parser.set('Main Settings', 'Admin password', admin_password)

    parser.write(config_file)


def read_config():
    parser = ConfigParser.SafeConfigParser()
    parser.read('telegram_settings.conf')

    for section_name in parser.sections():
            print 'Section:', section_name
            print '  Options:', parser.options(section_name)
            for name, value in parser.items(section_name):
                    print '  %s = %s' % (name, value)


def check_config():
    if not (os.path.isfile('telegram_settings.conf')):
        make_config()
