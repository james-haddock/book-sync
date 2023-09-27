

class Book:
    def __init__(self, UUID, load_from_db=False):
        self.UUID = UUID
        self.title = None
        self.cover = None
        self.textbook = None
        self.audiobook = None

        if load_from_db:
            from ..db.db_manager.db_manager_book import BookManager
            db_manager = BookManager()
            book_data = db_manager.get_book_by_uuid(UUID)

            if book_data:
                self.title = book_data.title
                self.cover = book_data.cover

                if db_manager.get_textbook_by_uuid(UUID):
                    from src.model.class_constructors.textbook.class_textbook import Textbook
                    self.textbook = Textbook(UUID, load_from_db=True)

                # if db_manager.get_audiobook_by_uuid(UUID):
                #     from .subclass_audiobook import Audiobook
                #     self.audiobook = Audiobook(UUID, load_from_db=True)
            else:
                print("No book found with the given UUID.")
        
    def add_textbook(self, textbook):
        self.textbook = textbook
        if not self.title:
            self.title = textbook.title
        if not self.cover:
            self.cover = textbook.cover

    def add_audiobook(self, audiobook):
        self.audiobook = audiobook
        if not self.title:
            self.title = audiobook.title
        if not self.cover:
            self.cover = audiobook.cover
