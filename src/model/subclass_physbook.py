import xml.etree.ElementTree as ET
# from class_book import Book


class Textbook:
    def __init__(self, filename, title='', author='', genre=''):
        # super().__init__(filename, title, author, genre)
        self.filename = filename
        self.container_namespace = '{urn:oasis:names:tc:opendocument:xmlns:container}'
        self.opf_namespace = '{http://www.idpf.org/2007/opf}'
        self.container_path = f'data/extracted/{self.filename}/META-INF/container.xml'
        self.opf = self.get_opf_location()
        self.opf_path = f'data/extracted/{self.filename}/{self.opf}'
        self.container_root = self.parse_and_get_root_xml(self.container_path)
        self.spine = self.get_spine()
        self.opf_root = self.parse_and_get_root_xml(self.opf_path)
        self.href = self.get_href()
        self.opf = self.get_opf_location()

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
        return spine
    
    def get_href(self):
        href = []
        for idref in self.spine:
            for element in self.opf_root.findall(f'{self.opf_namespace}manifest/{self.opf_namespace}item'):
                    if element.attrib['id'] == idref:
                        href.append(element.attrib['href'])
        return href