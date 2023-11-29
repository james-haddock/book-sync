import factory
from faker import Faker
from unittest.mock import MagicMock, patch
import pytest
from src.model.class_constructors.textbook.class_textbook import Textbook
import os
import uuid

class TextbookInitialiserFactory(factory.Factory):
    class Meta:
        model = MagicMock 

    faker = Faker()
    title = faker.sentence()
    cover = faker.file_path(extension='jpg')
    html_manager = MagicMock(get_consolidated_html_path=faker.file_path(extension='html'))

@pytest.fixture
def mock_textbook_initialiser():
    with patch('src.model.class_constructors.textbook.textbook_initialiser.TextbookInitialiser', new_callable=TextbookInitialiserFactory) as mock:
        yield mock

def test_textbook_initialization(mock_textbook_initialiser):
    test_uuid = str(uuid.uuid4())
    textbook = Textbook(test_uuid)
    mock_initialiser_instance = mock_textbook_initialiser.return_value
    assert textbook.UUID == test_uuid
    assert textbook.title == mock_initialiser_instance.title
    assert textbook.cover == mock_initialiser_instance.cover
    assert textbook.isbn == ''
    assert textbook.book_position == 0
    assert textbook.book_content == mock_initialiser_instance.html_manager.get_consolidated_html_path
    assert textbook.book_base == os.path.dirname(mock_initialiser_instance.html_manager.get_consolidated_html_path)
    mock_textbook_initialiser.assert_called_once_with(test_uuid)


src/tests/src/model/class_constructors/textbook/test_data