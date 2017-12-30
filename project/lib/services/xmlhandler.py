#!python3
import xml.etree.ElementTree as etree
from collections import defaultdict

from lib import queries
from lib.paths import *


class EDIm(object):
    def __init__(self, xmlFile, segmentIndicator):
        self.tree = etree.parse(xmlFile)
        self.root = self.tree.getroot()
        self.indexes = defaultdict(int)
        self.parsedData = []
        self.segmentIndicator = segmentIndicator
   
    # returns nodes that contain information children and will become table names in the future
    def get_nodes(self):

        for node in self.root.iterfind(".//*/[@" + self.segmentIndicator + "]"):
            
            # Update the segment ID dictionary or create if it does not exist
            if node.tag in self.indexes:
                self.indexes[node.tag] += 1
            else:
                self.indexes[node.tag] = 1
            
            nodeID = self.indexes[node.tag]

            # Create an array that contains the table name and a dictionary of columns/data
            table = [nodeID, node.tag, self.get_children(node)]
            # self.parsedData.extend(table)
            self.parsedData.append(table)


    # returns a dictionary with the children and their text for a specific segment
    def get_children(self, segment):
        result = dict()
        parent = self.get_parent(segment)
        
        # Insert the parent ID and name
        result['parentID'] = self.indexes[parent]
        result['parentName'] = parent

        for child in segment.findall('*'):
            if child.text != '/' and child.text != None and child.text != '*':
                result[child.tag] = child.text
        return result


    # Returns tag of direct parent of current segment
    def get_parent(self, segment):
        parent = self.tree.find('.//' + segment.tag + '[@SEGMENT]/..')
        return parent.tag
