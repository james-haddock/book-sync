import xml.etree.ElementTree as ET

class XmlParser:
    def __init__(self, xml_path):
        self.xml_path = xml_path
    
    def get_root(self):
        tree = ET.parse(self.xml_path)
        return tree.getroot()