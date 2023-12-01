import os
from src.model.class_constructors.textbook.xml_parser import XmlParser
from src.model.class_constructors.textbook.opf_extractor import OpfExtractor
from src.model.class_constructors.textbook.book_metadata_extractor import BookMetadataExtractor
from src.model.class_constructors.textbook.html_consolidation_manager import HtmlConsolidationManager
import logging

logging.basicConfig(level=logging.ERROR,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class TextbookInitialiser:
    def __init__(self, UUID):
        self.container_namespace = '{urn:oasis:names:tc:opendocument:xmlns:container}'
        self.container_path = f'src/book/{UUID}/META-INF/container.xml'
        
        container_parser = XmlParser(self.container_path)
        self.container_root = container_parser.get_root()
        
        self.opf = self.get_opf_location()
        self.opf_path = f'src/book/{UUID}/{self.opf}'
        self.opf_folder_location = os.path.dirname(self.opf_path)
        
        opf_parser = XmlParser(self.opf_path)
        self.opf_root = opf_parser.get_root()

        opf_extractor = OpfExtractor(self.opf_root)
        self.spine = opf_extractor.get_spine()
        self.href = opf_extractor.get_href(self.spine)

        metadata_extractor = BookMetadataExtractor(self.opf_root, self.opf_folder_location)
        self.title = metadata_extractor.get_title()
        self.cover = metadata_extractor.get_cover()

        self.html_manager = HtmlConsolidationManager(self.opf_folder_location, self.href, UUID)
        self.html_manager.consolidate_html_files()
           
    
    def get_opf_location(self):
        try:
            opf_location = self.container_root.find(f'{self.container_namespace}rootfiles/{self.container_namespace}rootfile').attrib['full-path']
            return opf_location
        except AttributeError:
            logger.error(f"Error: Could not find the attribute 'full-path' in XML.")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching OPF location: {e}")
            return None

        