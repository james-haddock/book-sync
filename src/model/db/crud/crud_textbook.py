from ..db_schema.db_schema import DBTextbook, DBBook, Association
from ...class_constructors.textbook.class_textbook import Textbook
from ..db_manager import DatabaseManager
from .crud_book import CrudBook

class CrudTextbook:

    @staticmethod
    def create_textbook_in_db(textbook: object, DBBook: object):
        with DatabaseManager() as session:
            db_textbook = DBTextbook(
                cover=textbook.cover,
                book_path=textbook.book_path,
                book_content=textbook.book_content,
                isbn=textbook.isbn,
                book_position=textbook.book_position
            )
            session.add(db_textbook)
            session.flush()

            association = Association(book_id=DBBook.id, book_type='DBTextbook', type_id=db_textbook.id)
            session.add(association)
            session.commit()

    @staticmethod
    def get_textbook_by_book_UUID(UUID):
        with DatabaseManager() as session:
            # Perform a join between DBBook, Association, and DBTextbook tables
            textbook = session.query(DBTextbook).\
                join(Association, Association.type_id == DBTextbook.id).\
                join(DBBook, DBBook.id == Association.book_id).\
                filter(DBBook.UUID == UUID, Association.book_type == 'DBTextbook').\
                first()

            return textbook

    @staticmethod
    def get_all_textbooks():
        with DatabaseManager() as session:
            textbooks = session.query(DBTextbook).all()
            return textbooks

    @staticmethod
    def update_textbook(textbook_id: int, **kwargs):
        with DatabaseManager() as session:
            textbook = session.query(DBTextbook).filter_by(id=textbook_id).first()
            if textbook:
                for key, value in kwargs.items():
                    setattr(textbook, key, value)
                session.commit()

    @staticmethod
    def delete_textbook(textbook_id: int):
        with DatabaseManager() as session:
            textbook = session.query(DBTextbook).filter_by(id=textbook_id).first()
            if textbook:
                association = session.query(Association).filter_by(type_id=textbook_id, book_type='textbook').first()
                if association:
                    session.delete(association)

                session.delete(textbook)
                session.commit()
