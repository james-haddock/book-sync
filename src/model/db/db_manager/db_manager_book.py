from ..db_schema.db_schema import DBBook
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker


class BookManager:
    def __init__(self, session):
        self.session = session

    def add_book(self, book):
        try:
            db_book = DBBook(
                UUID=book.UUID,
                title=book.title,
                cover=book.cover
            )
            self.session.add(db_book)
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred while adding book: {e}")

    def get_book_by_uuid(self, UUID):
        try:
            return self.session.query(DBBook).filter_by(UUID=UUID).first()
        except exc.SQLAlchemyError as e:
            print(f"Error occurred while retrieving book: {e}")
            return None

    def get_all_books(self):
        try:
            return self.session.query(DBBook).all()
        except exc.SQLAlchemyError as e:
            print(f"Error occurred while retrieving all books: {e}")
            return []

    def update_book(self, book):
        try:
            db_book = self.session.query(DBBook).filter_by(UUID=book.UUID).first()
            if db_book:
                db_book.title = book.title
                db_book.cover = book.cover
                self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred while updating book: {e}")

    def delete_book(self, UUID):
        try:
            db_book = self.session.query(DBBook).filter_by(UUID=UUID).first()
            if db_book:
                self.session.delete(db_book)
                self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred while deleting book: {e}")
