import uuid

class BookManager:
    def __init__(self):
        self.books = {}

    def add_book(self, book: object) -> str:
        self.books[book.UUID] = book
        print(f'{book.title} Book added to BookManager')

    def get_book(self, UUID: str) -> object:
        return self.books.get(UUID)