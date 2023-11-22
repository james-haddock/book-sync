from src.model.db.db_schema.db_schema import DBBook, Association, DBTextbook, DBAudiobook
from src.model.db.db_manager import DatabaseManager
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
import copy
import logging
from faker import Faker
from model.db.crud.crud_book import CrudBook
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

fake = Faker()

# @patch('ABReader.src.model.db.db_manager.DatabaseManager')
# def test_create_book_in_db(mock_db_manager):
#     fake_uuid = fake.uuid4()
#     fake_title = fake.text(max_nb_chars=20)

#     mock_book_type = MagicMock(spec=DBBook)
#     mock_book_type.UUID = fake_uuid
#     mock_book_type.title = fake_title

#     result = CrudBook.create_book_in_db(mock_book_type)

#     assert result is not None
#     assert result.UUID == fake_uuid
#     assert result.title == fake_title
