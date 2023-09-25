import os

class Textbook:
    def __init__(self, UUID, load_from_db=False):
        self.UUID = UUID
        if load_from_db:
            from .db_manager import DatabaseManager
            db_manager = DatabaseManager()
            textbook_data = db_manager.get_textbook_by_uuid(UUID)
            
            if textbook_data:
                self.title = textbook_data.title
                self.cover = textbook_data.cover
                self.book_path = textbook_data.book_path
                self.isbn = textbook_data.isbn
                self.book_position = textbook_data.book_position
            else:
                print("No textbook found with the given UUID.")
        else:
            from .textbook_initialiser import TextbookInitialiser
            initializer = TextbookInitialiser(UUID)
            self.title = initializer.title
            self.cover = initializer.cover
            self.book_path = os.path.dirname(initializer.opf_path)
            self.isbn = ''
            self.book_position = 0