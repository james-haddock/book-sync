from ..db_schema.db_schema import DBBook, Association, DBTextbook, DBAudiobook
from ..db_manager import DatabaseManager
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
import copy
from ...db.db_schema.db_schema import Base
import logging

# Setting up logging
logging.basicConfig(level=logging.ERROR,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

class CrudBook:
    
    @staticmethod
    def create_book_in_db(book_type: object):
        try:
            with DatabaseManager() as session:
                db_book = DBBook(UUID=book_type.UUID, title=book_type.title)
                session.add(db_book)
                session.flush()
                book = copy.deepcopy(db_book)
                return book
        except SQLAlchemyError as e:
            logger.error(f"Error creating book in database: {e}")
            return None
    
    @staticmethod
    def get_book(UUID):
        try:
            with DatabaseManager() as session:
                book = session.query(DBBook).filter_by(UUID=UUID).first()
                return book
        except SQLAlchemyError as e:
            logger.error(f"Error fetching book by UUID {UUID}: {e}")
            return None

    @staticmethod
    def get_book_with_details(session, UUID):
        try:
            book = session.query(DBBook).filter_by(UUID=UUID).first()
            if not book:
                return None

            associations = (session.query(Association)
                            .filter_by(book_id=book.id)
                            .all())

            book_versions = {}
            for association in associations:
                orm_class = globals().get(association.book_type)
                version_instance = session.query(orm_class).filter_by(id=association.type_id).first()
                if version_instance:
                    book_versions[association.book_type] = version_instance

            data = {'DBBook': book, **book_versions}
            return data
        except SQLAlchemyError as e:
            logger.error(f"Error fetching book details by UUID {UUID}: {e}")
            return None
    
    @staticmethod
    def get_all_books_with_details(session):
        try:
            books = (session.query(DBBook)
                    .options(joinedload(DBBook.associations))
                    .all())

            result = []

            for book in books:
                associations = book.associations
                book_versions = {}

                if associations:
                    for association in associations:
                        orm_class = globals().get(association.book_type)
                        version_instance = session.query(orm_class).filter_by(id=association.type_id).first()
                        if version_instance:
                            book_versions[association.book_type] = version_instance

                data = {'DBBook': book, **book_versions}
                result.append(data)

            return result
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all books with details: {e}")
            return []

    @staticmethod
    def update_book(UUID, **kwargs):
        try:
            with DatabaseManager() as session:
                book = session.query(DBBook).filter_by(UUID=UUID).first()
                if book:
                    for key, value in kwargs.items():
                        setattr(book, key, value)
                    session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error updating book by UUID {UUID}: {e}")

    @staticmethod
    def delete_book(UUID):
        try:
            with DatabaseManager() as session:
                book = session.query(DBBook).filter_by(UUID=UUID).first()
                if book:
                    session.delete(book)
                    session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Error deleting book by UUID {UUID}: {e}")
