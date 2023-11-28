import logging
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.ERROR,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class OpfExtractor:
    def __init__(self, root):
        self.root = root
        self.opf_namespace = '{http://www.idpf.org/2007/opf}'

    def get_spine(self):
        try:
            spine = [item.attrib['idref'] for item in self.root.findall(f'{self.opf_namespace}spine/{self.opf_namespace}itemref')]
            return spine
        except Exception as e:
            logger.error(f"Unexpected error while fetching spine from XML: {e}")
            return []

    def get_href(self, spine):
        try:
            href = []
            for idref in spine:
                for element in self.root.findall(f'{self.opf_namespace}manifest/{self.opf_namespace}item'):
                    if 'id' in element.attrib and element.attrib['id'] == idref:
                        href.append(element.attrib.get("href", ""))
            return href
        except Exception as e:
            logger.error(f"Unexpected error while fetching href from XML: {e}")
            return []
