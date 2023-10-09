import os

class Textbook:
    def __init__(self, UUID):
        from .textbook_initialiser import TextbookInitialiser
        initialiser: TextbookInitialiser = TextbookInitialiser(UUID)
        self.UUID: str = UUID
        self.title: str = initialiser.title
        self.cover: str = initialiser.cover
        self.isbn: int = ''
        self.book_position: int = 0
        self.book_content: str = initialiser.html_manager.get_consolidated_html_path
        self.book_base: str = os.path.dirname(self.book_content)