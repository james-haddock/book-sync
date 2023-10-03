from ..db_schema.db_schema import DBBook, Association, DBTextbook, DBAudiobook
from ..db_manager import DatabaseManager
from sqlalchemy.orm import joinedload
import copy
from ...db.db_schema.db_schema import Base


class CrudBook:
    
    @staticmethod
    def create_book_in_db(book_type: object):
        with DatabaseManager() as session:
            db_book = DBBook(UUID=book_type.UUID, title=book_type.title)
            session.add(db_book)
            session.flush()
            book = copy.deepcopy(db_book)
            return book

    @staticmethod
    def get_book(UUID):
        with DatabaseManager() as session:
            book = session.query(DBBook).filter_by(UUID=UUID).first()
            return book
    
    @staticmethod
    def get_book_with_details(session, UUID):
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

        data = {'book': book, **book_versions}

        return data

            
    @staticmethod
    def get_all_books_with_details(session):
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

            data = {'book': book, **book_versions}
            result.append(data)

        return result



            

    @staticmethod
    def update_book(UUID, **kwargs):
        with DatabaseManager() as session:
            book = session.query(DBBook).filter_by(UUID=UUID).first()
            if book:
                for key, value in kwargs.items():
                    setattr(book, key, value)
                session.commit()

    @staticmethod
    def delete_book(UUID):
        with DatabaseManager() as session:
            book = session.query(DBBook).filter_by(UUID=UUID).first()
            if book:
                session.delete(book)
                session.commit()



