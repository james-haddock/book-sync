
from .xml_parser import XmlParser
import os
from .opf_extractor import OpfExtractor
from .book_metadata_extractor import BookMetadataExtractor
from .class_book import Book
from .book_consolidator import HtmlConsolidator
from .html_consolidation_manager import HtmlConsolidationManager

class TextbookInitialiser:
    def __init__(self, UUID):
        self.container_namespace = '{urn:oasis:names:tc:opendocument:xmlns:container}'
        self.container_path = f'book/{UUID}/META-INF/container.xml'
        
        container_parser = XmlParser(self.container_path)
        self.container_root = container_parser.get_root()
        
        self.opf = self.get_opf_location()
        self.opf_path = f'book/{UUID}/{self.opf}'
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
        opf_location = self.container_root.find(f'{self.container_namespace}rootfiles/{self.container_namespace}rootfile').attrib['full-path']
        return opf_location