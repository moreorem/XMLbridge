import unittest
from ftplib import FTP


# Here's our "unit tests".
class TestUM(unittest.TestCase):

    def setUp(self):
        pass 

    def connect(self):
        ftp = FTP('192.168.16.66')
        try:
            ftp.login('delonghi', 'r3Mte0#6')
            print("File List: ")
            files = ftp.dir()
            print(files)
            return True
        except ConnectionError:
            print("Cannot connect!")


    def showdir(self, data):
        for line in data:
            print("-", line)

    
    def testOne(self):
        self.assertTrue(self.connect())

if __name__ == '__main__':
    unittest.main()