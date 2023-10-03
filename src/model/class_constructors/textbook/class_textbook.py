import os

class Textbook:
    def __init__(self, UUID):
        from .textbook_initialiser import TextbookInitialiser
        initialiser = TextbookInitialiser(UUID)
        self.UUID = UUID
        self.title = initialiser.title
        self.cover = initialiser.cover
        self.book_path = os.path.dirname(initialiser.opf_path)
        self.isbn = ''
        self.book_position = 0
        self.book_content = initialiser.html_manager.get_consolidated_html_path