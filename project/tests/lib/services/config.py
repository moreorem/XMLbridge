#!python3
from configparser import *


class Config(object):
    @staticmethod
    def load(file):
        config = RawConfigParser()
        configFilePath = file
        config.read(configFilePath)

        try:
            use_anonymous = config.get('other', 'use_anonymous')

        except NoOptionError :
            print('Could not read configuration file')
            sys.exit(1)
        return config

    def list_config(file):
        config = Config.load(file)

        # List all contents
        print("List all contents")
        for section in config.sections():
            print("Section: %s" % section)
            for options in config.options(section):
                print("x %s:::%s:::%s" % (options, config.get(section, options), str(type(options))))


        # # Print some contents
        # print("\nPrint some contents")
        # print(config.get('other', 'use_anonymous'))  # Just get the value
        # print(config.getboolean('other', 'use_anonymous'))  # You know the datatype?


if __name__ == "__main__":
    Config.load("./project/config.cfg")