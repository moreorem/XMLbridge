import unittest
import os
import yaml

class TestUM(unittest.TestCase):
    MAIN_DIRECTORY = os.path.abspath("")
    CONFIG_NAME = 'config.yml'

    def setUp(self):
        pass 

    def getfullpath(self):
        return self.MAIN_DIRECTORY + '\\project\\'

    def getdirectory(self, section):
        with open(self.getfullpath() + self.CONFIG_NAME) as ymlfile:
            cfg = yaml.load(ymlfile)
        return cfg['directories'][section]

    def test_getmainpath(self):
        print( self.getfullpath())
        assert len(self.getfullpath()) > 0

    def test_config(self):
        print(self.getdirectory('xml'))
        

if __name__ == '__main__':
    unittest.main()

