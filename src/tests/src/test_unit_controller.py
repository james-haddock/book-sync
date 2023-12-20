import pytest
from flask import Flask, request, session, url_for
from unittest.mock import patch, MagicMock
from werkzeug.datastructures import FileStorage
from src.controller import upload, app
from src.model.db.db_schema.db_schema import DBTextbook

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_get(client):
    response = client.get('/upload')
    assert response.status_code == 200

@patch('src.controller.epub_validator')
@patch('src.controller.extract_book.extractbook')
@patch('src.controller.class_textbook.Textbook')
@patch('src.controller.crud_book.create_book_in_db')
@patch('src.controller.crud_textbook.create_textbook_in_db')
@patch('src.controller.s3_crud.upload_to_s3')
def test_upload_post_valid_epub(mock_upload_to_s3, mock_create_textbook_in_db, mock_create_book_in_db, mock_Textbook, mock_extractbook, mock_epub_validator, client):
    mock_epub_validator.return_value = True
    mock_file = MagicMock(spec=FileStorage)
    mock_file.filename = 'test.epub'
    data = {
        'file': (mock_file, 'test.epub')
    }
    with client.session_transaction() as session:
        response = client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        assert ('message', 'Book uploaded successfully!') in session['_flashes']

@patch('src.controller.epub_validator')
def test_upload_post_invalid_epub(mock_epub_validator, client):
    mock_epub_validator.return_value = False
    mock_file = MagicMock(spec=FileStorage)
    mock_file.filename = 'test.epub'
    data = {
        'file': (mock_file, 'test.epub')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    with client.session_transaction() as session:
        assert ('message', 'Invalid file. Only valid EPUB files are allowed.') in session['_flashes']

def test_upload_post_no_file(client):
    response = client.post('/upload', content_type='multipart/form-data')
    assert response.status_code == 400
    with client.session_transaction() as session:
        assert ('message', 'No file selected') in session['_flashes']
        
@patch('src.controller.crud_book.get_all_books_with_details')
@patch('src.controller.change_urls_to_presigned.generate_presigned_url')
def test_library(mock_generate_presigned_url, mock_get_all_books_with_details, client):
    mock_book = {
        'DBTextbook': DBTextbook(cover='cover_url'),
        'other_details': 'details'
    }
    mock_get_all_books_with_details.return_value = [mock_book]
    mock_generate_presigned_url.return_value = 'presigned_url'

    response = client.get('/library')

    assert response.status_code == 200
    assert b'presigned_url' in response.data
    mock_get_all_books_with_details.assert_called_once()
    mock_generate_presigned_url.assert_called_once_with(aws_bucket, 'cover_url', s3)

def test_book_route_success():
    with patch('controller.crud_book.get_book_with_details') as mock_get_book_with_details, \
         patch('controller.get_s3_object_content') as mock_get_s3_object_content, \
         patch('controller.save_book_session_js') as mock_save_book_session_js:
        
        mock_get_book_with_details.return_value = {
            'DBTextbook': MagicMock(book_content='content'),
            'DBBook': MagicMock(title='title')
        }
        mock_get_s3_object_content.return_value = 'html_content'
        mock_save_book_session_js.return_value = 'save_book_session_js'

        with app.test_client() as client:
            response = client.get(url_for('book', UUID='123'))
            assert response.status_code == 200
            assert b'title' in response.data
            assert b'123' in response.data
            assert b'save_book_session_js' in response.data

def test_book_route_failure():
    with patch('controller.crud_book.get_book_with_details') as mock_get_book_with_details, \
         patch('controller.get_s3_object_content') as mock_get_s3_object_content:
        
        mock_get_book_with_details.return_value = {
            'DBTextbook': MagicMock(book_content='content'),
            'DBBook': MagicMock(title='title')
        }
        mock_get_s3_object_content.return_value = None

        with app.test_client() as client:
            response = client.get(url_for('book', UUID='123'))
            assert response.status_code == 500