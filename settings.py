__author__ = 'nikolaev'
import ConfigParser


def make_config():
    admin_id = raw_input("Enter admin id in telegram:")
    token = raw_input("Enter token for your bot:")
    admin_password = raw_input("Enter password for access your bot not only with your device:")
    parser = ConfigParser.SafeConfigParser()
    config_file = open("telegram_settings.conf", "w")
    parser.add_section('[Main Settings]')

    parser.set('[Main Settings]', 'admin_id', admin_id)
    parser.set('[Main Settings]', 'Token', token)
    parser.set('[Main Settings]', 'Admin password', admin_password)


    for section in parser.sections():
        print section
        for name, value in parser.items(section):
            print '  %s = %r' % (name, value)

    parser.write(config_file)

make_config()