from src.model.class_constructors.class_book import Book
import uuid

def test_textbook_initialization():
    test_uuid = str(uuid.uuid4())
    book = Book(test_uuid)

    assert book.UUID == test_uuid
    assert book.title == None
    assert book.cover == None
    assert book.textbook == None
    assert book.audiobook == None