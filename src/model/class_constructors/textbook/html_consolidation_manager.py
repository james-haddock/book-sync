
import os
from src.model.class_constructors.textbook.book_consolidator import HtmlConsolidator

class HtmlConsolidationManager:
    def __init__(self, opf_folder_location: str, href: list, UUID:str):
        self.html_consolidator = HtmlConsolidator()
        self.opf_folder_location = opf_folder_location
        self.href = href
        self.UUID = UUID

    @property
    def get_html_directory(self):
        return os.path.dirname(os.path.join(self.opf_folder_location, self.href[1]))

    @property
    def get_href_relative_path(self):
        return [self.opf_folder_location + '/' + URL for URL in self.href]

    @property
    def get_consolidated_html_path(self):
        return f'src/book/{self.UUID}/consolidated_{self.UUID}.html'

    def consolidate_html_files(self):
        self.html_consolidator.consolidate_html(self.get_href_relative_path, self.get_consolidated_html_path, self.UUID)
