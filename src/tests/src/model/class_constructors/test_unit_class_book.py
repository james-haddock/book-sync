from src.model.class_constructors.class_book import Book
import uuid

def test_book():
    test_uuid = str(uuid.uuid4())
    book = Book(uuid)
    assert book.UUID == uuid
    assert book.title == None
    assert book.cover == None
    assert book.textbook == None
    assert book.audiobook == None