import xml.etree.ElementTree as ET
import os
from .textbook_initialiser import TextbookInitialiser
class Textbook:
    def __init__(self, UUID):
        initializer = TextbookInitialiser(UUID)
        self.UUID = UUID
        self.title = initializer.title
        self.cover = initializer.cover
        self.href = initializer.href
        self.book_path = os.path.dirname(initializer.opf_path)
        self.isbn = ''
        self.book_index_number = 20

