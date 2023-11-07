import os
import logging

logging.basicConfig(level=logging.ERROR,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class BookMetadataExtractor:
    def __init__(self, opf_root, opf_folder_location):
        self.opf_folder_location = opf_folder_location
        self.opf_root = opf_root
        self.opf_namespace = '{http://www.idpf.org/2007/opf}'
        self.DC_namespace = '{http://purl.org/dc/elements/1.1/}'

    def get_title(self):
        try:
            return self.opf_root.find(f'{self.opf_namespace}metadata/{self.DC_namespace}title').text
        except AttributeError:
            logger.error("Error: Could not extract title from XML.")
            return None

    def get_cover(self):
        cover_loc = None
        try:
            for element in self.opf_root.findall(f'{self.opf_namespace}manifest/{self.opf_namespace}item'):
                if element.attrib.get('id') == 'cover-image' or element.attrib.get('properties') == 'cover-image':
                    cover_loc = element.attrib.get('href')
                else:    
                    for element in self.opf_root.findall(f'{self.opf_namespace}metadata/{self.opf_namespace}meta'):
                        if element.attrib.get('name') == 'cover':
                            cover_id = element.attrib.get('content')
                            for item in self.opf_root.findall(f'{self.opf_namespace}manifest/{self.opf_namespace}item'):
                                if item.attrib.get('id') == cover_id:
                                    cover_loc = item.attrib.get('href')
            if cover_loc:
                print('Cover retrieved')
                return os.path.join(self.opf_folder_location, cover_loc)
            else:
                logger.error("Error: Could not extract cover location from XML. Using palceholder")
                return 'static/Book-icon.png'
        except Exception as e:
            logger.error(f"Unexpected error while fetching cover from XML: {e}")
            return None
