import unittest
import xml.etree.ElementTree as etree
from lib import queries
from lib.services import connection

class TestUM(unittest.TestCase):
 
    def setUp(self):
        pass
    
    def printchildren(self, root):
        for child in root:
            print(child)

    def loadxml(self, filepath):
        tree = etree.parse(filepath)
        root = tree.getroot()
        return root

    def downloadxml(self, formId):
        file_name = paths.getfullpath() + 'form_' + formId + '.xml'
        self.db = connection.DBsqlsrv('sa', '5268', 'OMIROS\SQL2008R2')
        self.cur = queries.getFormXML(self.db, 'GoldLed', formId)
        lines = 0
        with open(file_name, 'w') as x:
            x.write('<?xml version="1.0" encoding="utf-8"?>\n')
            x.write("<form>\n")
            for row in self.cur:
                x.write(str(row[1]))
                lines += 1
            x.write("\n</form>")
            
        x.close()
        self.db.con.close()
        return lines
               

    def showattribute(self, element):
        root = self.loadxml(r'D:\orestes\Projects\Python\FormManager\project\components\ribbonControlFromTo.xml')
        return root[element].attrib

    def test_xml_download(self):
        assert self.downloadxml('113') > 0

    def test_xml_load(self):
        assert print(self.loadxml(r'D:\orestes\Projects\Python\FormManager\project\components\ribbonControlFromTo.xml')) != ''
 
    def test_xml_children(self):
        assert print(self.printchildren(self.loadxml(r'D:\orestes\Projects\Python\FormManager\project\components\ribbonControlFromTo.xml'))) != ''

    def test_xml_attribute(self):
        assert print(self.showattribute(4)) != ''

if __name__ == '__main__':
    unittest.main()