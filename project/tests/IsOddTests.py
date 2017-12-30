import unittest
import pymssql
import configparser
# Here's our "unit".
def connect_database(config):
    print('')


def read_config(cFile):
    cfg = configparser.ConfigParser()
    cfg.read(cFile)
    cfg.sections()
    
    return cfg.get('DEFAULT', 'serveraliveinterval')




# Here's our "unit tests".
class ConnectionTests(unittest.TestCase):

    def testOne(self):
        self.assertTrue(read_config('../config.ini'))
        
    # def testTwo(self):
    #     self.assertFalse(IsOdd(2))

    # def testThree(self):
    #     self.assertTrue(ftp.command(address = 'ftp3.goldair.gr', username = 'delonghi', password = 'r3Mte0#6', sshport = '6933' ))






def main():
    unittest.main()


if __name__ == '__main__':
    main()