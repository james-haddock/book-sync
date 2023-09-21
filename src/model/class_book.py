
class Book:
    def __init__(self, UUID: str):
        self.UUID = UUID
        self.title = None
        self.cover = None
        self.textbook = None
        self.audiobook = None

    def add_textbook(self, textbook: object):
        self.textbook = textbook
        if not self.title:
            self.title = textbook.title
        if not self.cover:
            self.cover = textbook.cover

    def add_audiobook(self, audiobook: object):
        self.audiobook = audiobook
        if not self.title:
            self.title = audiobook.title
        if not self.cover:
            self.cover = audiobook.cover