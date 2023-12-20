import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError
from src.model.db.crud.crud_textbook import CrudTextbook

def test_create_textbook_in_db_success():
    textbook = MagicMock(cover='cover', book_content='content', isbn='isbn', book_position='position', book_base='base')
    DBBook = MagicMock(id=1)

    with patch('src.model.db.crud.crud_textbook.DBTextbook', return_value=MagicMock()) as mock_DBTextbook, \
         patch('src.model.db.crud.crud_textbook.Association', return_value=MagicMock()) as mock_Association, \
         patch('src.model.db.crud.crud_textbook.DatabaseManager') as mock_DatabaseManager:

        mock_session = mock_DatabaseManager.return_value.__enter__.return_value

        CrudTextbook.create_textbook_in_db(textbook, DBBook)

        mock_DBTextbook.assert_called_once_with(
            cover='cover',
            book_content='content',
            isbn='isbn',
            book_position='position',
            book_base='base'
        )
        mock_Association.assert_called_once_with(book_id=1, book_type='DBTextbook', type_id=mock_DBTextbook.return_value.id)
        mock_session.add.assert_any_call(mock_DBTextbook.return_value)
        mock_session.add.assert_any_call(mock_Association.return_value)
        mock_session.commit.assert_called_once()

def test_create_textbook_in_db_failure():
    textbook = MagicMock(cover='cover', book_content='content', isbn='isbn', book_position='position', book_base='base')
    DBBook = MagicMock(id=1)

    with patch('src.model.db.crud.crud_textbook.DBTextbook', return_value=MagicMock()) as mock_DBTextbook, \
         patch('src.model.db.crud.crud_textbook.Association', return_value=MagicMock()) as mock_Association, \
         patch('src.model.db.crud.crud_textbook.DatabaseManager') as mock_DatabaseManager, \
         patch('src.model.db.crud.crud_textbook.logger') as mock_logger:

        mock_session = mock_DatabaseManager.return_value.__enter__.return_value
        mock_session.commit.side_effect = SQLAlchemyError

        CrudTextbook.create_textbook_in_db(textbook, DBBook)

        mock_logger.error.assert_called_once()