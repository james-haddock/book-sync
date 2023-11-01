import logging
from sqlalchemy.exc import SQLAlchemyError
from ..db_schema.db_schema import DBTextbook, DBBook, Association
from ...class_constructors.textbook.class_textbook import Textbook
from ..db_manager import DatabaseManager
from .crud_book import CrudBook

logging.basicConfig(level=logging.ERROR,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

class CrudTextbook:

    @staticmethod
    def create_textbook_in_db(textbook: object, DBBook: object):
        try:
            with DatabaseManager() as session:
                db_textbook = DBTextbook(
                    cover=textbook.cover,
                    book_content=textbook.book_content,
                    isbn=textbook.isbn,
                    book_position=textbook.book_position,
                    book_base=textbook.book_base
                )
                session.add(db_textbook)
                session.flush()

                association = Association(book_id=DBBook.id, book_type='DBTextbook', type_id=db_textbook.id)
                session.add(association)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error creating textbook in database: {e}")

    @staticmethod
    def get_textbook_by_book_UUID(UUID):
        try:
            with DatabaseManager() as session:
                textbook = session.query(DBTextbook)\
                    .join(Association, Association.type_id == DBTextbook.id)\
                    .join(DBBook, DBBook.id == Association.book_id)\
                    .filter(DBBook.UUID == UUID, Association.book_type == 'DBTextbook').first()
                return textbook
        except SQLAlchemyError as e:
            logger.error(f"Error fetching textbook by UUID {UUID}: {e}")
            return None

    @staticmethod
    def get_all_textbooks():
        try:
            with DatabaseManager() as session:
                textbooks = session.query(DBTextbook).all()
                return textbooks
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all textbooks: {e}")
            return []

    @staticmethod
    def update_textbook(textbook_id: int, **kwargs):
        try:
            with DatabaseManager() as session:
                textbook = session.query(DBTextbook).filter_by(id=textbook_id).first()
                if textbook:
                    for key, value in kwargs.items():
                        setattr(textbook, key, value)
                    session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error updating textbook with ID {textbook_id}: {e}")

    @staticmethod
    def delete_textbook(textbook_id: int):
        try:
            with DatabaseManager() as session:
                textbook = session.query(DBTextbook).filter_by(id=textbook_id).first()
                if textbook:
                    association = session.query(Association).filter_by(type_id=textbook_id, book_type='textbook').first()
                    if association:
                        session.delete(association)
                    session.delete(textbook)
                    session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error deleting textbook with ID {textbook_id}: {e}")
