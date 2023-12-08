from src.model.class_constructors.textbook.epub_validator import validate_book
import pytest
from unittest.mock import patch, PropertyMock

@pytest.mark.unit
def test_validate_book():
    assert validate_book("src/tests/src/model/class_constructors/textbook/test_data/The Pragmatic Programmer- Your Journey To Mastery, 20th -- Andrew Hunt; David Hurst Thomas -- 2nd, Hardcover, 2019 -- Addison-Wesley Professional -- 9780135957059 -- 392cffdf0397e654c60b47a8fe54682f -- Anna’s Archive.epub")

@pytest.mark.unit
def test_invalid_book_exception():
    with patch('src.model.class_constructors.textbook.epub_validator.logger') as mock_logger:
        book = 'non/existant/book.epub'
        with pytest.raises(Exception):
            validate_book(book)
        mock_logger.error.assert_called_once_with(f"EPUB validation failed for {book}.")

@pytest.mark.unit
@patch('src.model.class_constructors.textbook.epub_validator.EpubCheck')
def test_epubcheck_runtime_exception(mock_epubcheck):
    type(mock_epubcheck.return_value).valid = PropertyMock(side_effect=RuntimeError('simulated runtime error'))

    with patch('src.model.class_constructors.textbook.epub_validator.logger') as mock_logger:
        book = 'some/book.epub'

        with pytest.raises(RuntimeError) as exc_info:
            validate_book(book)
        assert str(exc_info.value) == 'simulated runtime error'
        mock_logger.exception.assert_called_once()
