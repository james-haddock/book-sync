import os

class BookMetadataExtractor:
    def __init__(self, opf_root, opf_folder_location):
        self.opf_folder_location = opf_folder_location
        self.opf_root = opf_root
        self.opf_namespace = '{http://www.idpf.org/2007/opf}'
        self.DC_namespace = '{http://purl.org/dc/elements/1.1/}'

    def get_title(self):
        return self.opf_root.find(f'{self.opf_namespace}metadata/{self.DC_namespace}title').text
    
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
        print('Cover retrieved')
        return f'{self.opf_folder_location}/{cover_loc}'