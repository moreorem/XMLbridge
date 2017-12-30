#!python3
import configparser
import io


class Config(object):
    @staticmethod
    def load(file):
        with open(file) as f:
            sample_config = f.read()
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read_file(sample_config)
        

        # List all contents
        print("List all contents")
        for section in config.sections():
            print("Section: %s" % section)
            for options in config.options(section):
                print("x %s:::%s:::%s" % (options, config.get(section, options), str(type(options))))


        # Print some contents
        print("\nPrint some contents")
        print(config.get('other', 'use_anonymous'))  # Just get the value
        print(config.getboolean('other', 'use_anonymous'))  # You know the datatype?
        return config.get('other', 'use_anonymous')