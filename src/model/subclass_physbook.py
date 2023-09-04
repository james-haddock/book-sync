import xml.etree.ElementTree as ET
import os
import uuid

class Textbook:
    def __init__(self, UUID):
        self.UUID = UUID 
        self.container_namespace = '{urn:oasis:names:tc:opendocument:xmlns:container}'
        self.opf_namespace = '{http://www.idpf.org/2007/opf}'
        self.container_path = f'data/{self.UUID}/META-INF/container.xml'
        self.opf = self.get_opf_location()
        self.opf_path = f'data/{self.UUID}/{self.opf}'
        self.opf_folder_location = os.path.dirname(self.opf_path)
        # self.book_path = "/".join(self.opf_folder_location.split('/')[3:])
        self.book_path = self.opf_folder_location
        self.container_root = self.parse_and_get_root_xml(self.container_path)
        self.spine = self.get_spine()
        self.opf_root = self.parse_and_get_root_xml(self.opf_path)
        self.href = self.get_href()
        self.opf = self.get_opf_location()
        self.title = self.get_title()
        self.cover = self.get_cover()
        self.isbn = ''
        self.book_index_number = 20
        self.scroll_position = ''

    def parse_and_get_root_xml(self, xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()
        return root

    def get_opf_location(self):
        root = self.parse_and_get_root_xml(self.container_path)
        opf_location = root.find(f'{self.container_namespace}rootfiles/{self.container_namespace}rootfile').attrib['full-path']
        return opf_location
    
    def get_spine(self):
        root = self.parse_and_get_root_xml(self.opf_path)
        spine = [item.attrib['idref'] for item in root.findall(f'{self.opf_namespace}spine/{self.opf_namespace}itemref')]
        print('Spine retrieved')
        return spine
    
    def get_href(self):
        href = []
        for idref in self.spine:
            for element in self.opf_root.findall(f'{self.opf_namespace}manifest/{self.opf_namespace}item'):
                    if element.attrib['id'] == idref:
                        href.append(f'{element.attrib["href"]}')
        print('Compiled href list')
        return href
    
    def get_cover(self):
        if self.opf_root.attrib['version'] == '3.0':
            for element in self.opf_root.findall(f'{self.opf_namespace}manifest/{self.opf_namespace}item'):
                if element.attrib['id'] == 'cover-image':
                    cover_loc = element.attrib['href']
        elif self.opf_root.attrib['version'] == '2.0':
            for element in self.opf_root.findall(f'{self.opf_namespace}metadata/{self.opf_namespace}meta'):
                if element.attrib['name'] == 'cover':
                    cover_id = element.attrib['content']
                    for item in self.opf_root.findall(f'{self.opf_namespace}manifest/{self.opf_namespace}item'):
                        if item.attrib['id'] == cover_id:
                            cover_loc = item.attrib['href']
        opf_folder_location = os.path.dirname(self.opf_path)
        print('Cover retrieved')
        return f'{opf_folder_location}/{cover_loc}'
    
    def get_title(self):
        DC_namespace = '{http://purl.org/dc/elements/1.1/}'
        return self.opf_root.find(f'{self.opf_namespace}metadata/{DC_namespace}title').text