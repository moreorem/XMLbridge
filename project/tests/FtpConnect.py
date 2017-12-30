import unittest
from ftplib import FTP_TLS

# Here's our "unit".
def connect(self):
    ftps = FTP('ftp3.goldair.gr')
    ftps.login(user = 'delonghi', passwd = 'r3Mte0#6')
    ftps.prot_p()          # switch to secure data connection
    ftps.retrlines('LIST') # list directory content securely
    print(ftps.retrlines('LIST'))
    ftps.quit()
    
# Here's our "unit tests".
class IsOddTests(unittest.TestCase):

    def testOne(self):
        self.assertTrue(connect())

   
def main():
    unittest.main()

