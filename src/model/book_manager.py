import uuid

class BookManager:
    def __init__(self):
        self.books = {}

    def generate_book_instance_id(self) -> str:
        book_instance_id = str(uuid.uuid4())
        return book_instance_id

    def add_book(self, book: object) -> str:
        book_instance_id = self.generate_book_instance_id()
        self.books[book_instance_id] = book
        return book_instance_id

    def get_book(self, book_instance_id: str) -> object:
        return self.books.get(book_instance_id)