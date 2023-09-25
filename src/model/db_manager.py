
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from .db_schema import Base, DBBook, DBTextbook, DBAudiobook
from .class_book import Book
from .subclass_physbook import Textbook

class DatabaseManager:
    def __init__(self):
        DATABASE_URL = "postgresql://james:data0303@localhost:5432/booksync"
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)

    # Create
    def add_book(self, book):
        session = self.Session()
        try:
            db_book = DBBook(
                UUID=book.UUID,
                title=book.title,
                cover=book.cover
            )
            session.add(db_book)
            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            print(f"Error occurred while adding book: {e}")
        finally:
            session.close()

    def add_textbook(self, textbook):
        session = self.Session()
        try:
            db_textbook = DBTextbook(
                title=textbook.title,
                cover=textbook.cover,
                book_path=textbook.book_path,
                isbn=textbook.isbn,
                book_position=textbook.book_position
            )
            session.add(db_textbook)
            session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            print(f"Error occurred while adding textbook: {e}")
        finally:
            session.close()

    # Read
    def get_book_by_uuid(self, UUID):
        session = self.Session()
        try:
            book = session.query(DBBook).filter_by(UUID=UUID).first()
            return book
        except exc.SQLAlchemyError as e:
            print(f"Error occurred while retrieving book: {e}")
        finally:
            session.close()

    def get_textbook_by_uuid(self, UUID):
        session = self.Session()
        try:
            textbook = session.query(DBTextbook).filter_by(book_id=UUID).first()
            return textbook
        except exc.SQLAlchemyError as e:
            print(f"Error occurred while retrieving textbook: {e}")
        finally:
            session.close()

    def get_all_books(self):
        session = self.Session()
        try:
            all_books = session.query(DBBook).all()
            return all_books
        except exc.SQLAlchemyError as e:
            print(f"Error occurred while retrieving all books: {e}")
        finally:
            session.close()

    def load_books_with_details(self):
        books_data = self.get_all_books()
        books = []

        for book_data in books_data:
            book = Book(book_data.UUID, load_from_db=True)
            
            textbook_data = self.get_textbook_by_uuid(book_data.UUID)
            if textbook_data:
                book.textbook = Textbook(textbook_data.UUID, load_from_db=True)
            
            # audiobook_data = self.get_audiobook_by_uuid(book_data.UUID)
            # if audiobook_data:
            #     book.audiobook = Audiobook(audiobook_data.UUID, load_from_db=True)

            books.append(book)

        return books

    # Update
    def update_book(self, book):
        session = self.Session()
        try:
            db_book = session.query(DBBook).filter_by(UUID=book.UUID).first()
            if db_book:
                db_book.title = book.title
                db_book.cover = book.cover
                session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            print(f"Error occurred while updating book: {e}")
        finally:
            session.close()

    def update_textbook(self, textbook):
        session = self.Session()
        try:
            db_textbook = session.query(DBTextbook).filter_by(book_id=textbook.UUID).first()
            if db_textbook:
                db_textbook.title = textbook.title
                db_textbook.cover = textbook.cover
                db_textbook.book_path = textbook.book_path
                db_textbook.isbn = textbook.isbn
                db_textbook.book_position = textbook.book_position
                session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            print(f"Error occurred while updating textbook: {e}")
        finally:
            session.close()

    # Delete
    def delete_book(self, UUID):
        session = self.Session()
        try:
            db_book = session.query(DBBook).filter_by(UUID=UUID).first()
            if db_book:
                session.delete(db_book)
                session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            print(f"Error occurred while deleting book: {e}")
        finally:
            session.close()

    def delete_textbook(self, UUID):
        session = self.Session()
        try:
            db_textbook = session.query(DBTextbook).filter_by(book_id=UUID).first()
            if db_textbook:
                session.delete(db_textbook)
                session.commit()
        except exc.SQLAlchemyError as e:
            session.rollback()
            print(f"Error occurred while deleting textbook: {e}")
        finally:
            session.close()
