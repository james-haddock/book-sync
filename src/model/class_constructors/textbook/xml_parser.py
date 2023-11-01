import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.ERROR,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class XmlParser:
    def __init__(self, xml_path):
        self.xml_path = xml_path
    
    def get_root(self):
        try:
            tree = ET.parse(self.xml_path)
            return tree.getroot()
        except ET.ParseError as e:
            logger.error(f"Error parsing XML file at {self.xml_path}: {e}")
            return None
        except FileNotFoundError:
            logger.error(f"XML file not found at {self.xml_path}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while parsing XML file at {self.xml_path}: {e}")
            return None