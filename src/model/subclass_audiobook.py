from class_book import Book

class Audiobook(Book):
    def __init__(self, title):

        super().__init__(title)
        self.title = title
    