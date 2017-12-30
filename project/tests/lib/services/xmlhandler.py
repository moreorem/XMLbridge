#!python3
from xml import etree
import xml.etree.ElementTree as elt

class FormXml(object):
    def __init__(self, *args):
        try:
            self.args = dict(args)
        except TypeError:
            print('wrong parameters are passed')
            pass

        self.xmlData = elt.parse("components\empty.xml")
        
    def get_xml(self):
        return self.xmlData.getroot()

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
        

"""
import os, os.path, sys
import glob
from xml.etree import ElementTree
def run(files):
    xml_files = glob.glob(files +"/*.xml")
    xml_element_tree = None
    for xml_file in xml_files:
        data = ElementTree.parse(xml_file).getroot()
        # print ElementTree.tostring(data)
        for result in data.iter('results'):
            if xml_element_tree is None:
                xml_element_tree = data 
                insertion_point = xml_element_tree.findall("./results")[0]
            else:
                insertion_point.extend(result) 
    if xml_element_tree is not None:
        print ElementTree.tostring(xml_element_tree)

"""