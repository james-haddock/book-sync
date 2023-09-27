from ..db_schema.db_schema import DBTextbook
from sqlalchemy import create_engine, exc

class TextbookManager:
    def __init__(self, session):
        self.session = session

    def add_textbook(self, textbook):
        try:
            db_textbook = DBTextbook(
                title=textbook.title,
                cover=textbook.cover,
                book_path=textbook.book_path,
                isbn=textbook.isbn,
                book_position=textbook.book_position
            )
            self.session.add(db_textbook)
            self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred while adding textbook: {e}")

    def get_textbook_by_uuid(self, UUID):
        try:
            return self.session.query(DBTextbook).filter_by(book_id=UUID).first()
        except exc.SQLAlchemyError as e:
            print(f"Error occurred while retrieving textbook: {e}")
            return None

    def update_textbook(self, textbook):
        try:
            db_textbook = self.session.query(DBTextbook).filter_by(book_id=textbook.UUID).first()
            if db_textbook:
                db_textbook.title = textbook.title
                db_textbook.cover = textbook.cover
                db_textbook.book_path = textbook.book_path
                db_textbook.isbn = textbook.isbn
                db_textbook.book_position = textbook.book_position
                self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred while updating textbook: {e}")

    def delete_textbook(self, UUID):
        try:
            db_textbook = self.session.query(DBTextbook).filter_by(book_id=UUID).first()
            if db_textbook:
                self.session.delete(db_textbook)
                self.session.commit()
        except exc.SQLAlchemyError as e:
            self.session.rollback()
            print(f"Error occurred while deleting textbook: {e}")
