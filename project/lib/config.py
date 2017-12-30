# from ConfigParser import SafeConfigParser
import configparser, base64

config = configparser.ConfigParser()
config['DEFAULT'] = {'ServerAliveInterval': '45'}

sqlsrv =    {
                'host': 'OMIROS\SQL2008R2',
                'user': 'sa',
                'passwd': '5268',
                'db': 'test'
            }









# config = SafeConfigParser()
# config.read('config.ini')
# config.add_section('main')
# config.set('main', 'key1', 'value1')
# config.set('main', 'key2', 'value2')
# config.set('main', 'key3', 'value3')

with open('config.ini', 'w') as configFile:
    config.write(configFile)