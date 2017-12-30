import unittest
import pymssql

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def connect(self, userIn, passwordIn, hostIn):
        try:
            self.con = pymssql.connect(user = userIn, password = passwordIn, host = r'' + hostIn, database = '' , timeout = 8, autocommit = True)
            self.cur = self.con.cursor()
            print("connection successful!")
        except:
            print("Connection Failed ")

    def test_connection(self):
        assert self.connect('sa', '5268', 'OMIROS\SQL2008R2') != Exception

if __name__ == '__main__':
    unittest.main()