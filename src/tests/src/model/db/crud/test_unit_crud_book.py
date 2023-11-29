from src.model.db.db_schema.db_schema import DBBook, Association, DBTextbook, DBAudiobook
from src.model.db.db_manager import DatabaseManager
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
import copy
import logging
from faker import Faker
from src.model.db.crud.crud_book import CrudBook
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.tests.src.model.db.crud.crud_factories import DBBookFactory

fake = Faker()

def test_create_book_in_db(db_url):
    with pytest.MonkeyPatch.context() as m:
        m.setenv("DATABASE_URL", db_url)
        test_book = DBBookFactory()
        with DatabaseManager() as new_session:
            result = CrudBook.create_book_in_db(test_book)
            assert result is not None
            assert result.UUID == test_book.UUID
            assert result.title == test_book.title

        with DatabaseManager() as new_session:
            db_book = new_session.query(DBBook).filter_by(UUID=test_book.UUID).first()
            assert db_book is not None
            assert db_book.title == test_book.title