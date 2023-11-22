import tempfile
from flask import url_for, flash
from unittest.mock import MagicMock
from controller import s3, aws_bucket
import uuid
from faker import Faker

fake = Faker()

def test_upload_success(client, book_factory, mock_external_dependencies):
    # Create a temporary file for testing
    _, temp_file_path = tempfile.mkstemp(suffix=".epub")
    with open(temp_file_path, "w") as temp_file:
        temp_file.write("This is a dummy EPUB file.")

    # Create fake data using a factory
    fake_title = fake.text(max_nb_chars=50)
    fake_uuid = str(uuid.uuid4())

    # Unpack the mocked external dependencies
    mock_extractbook, mock_create_textbook_in_db, mock_create_book_in_db, mock_upload_to_s3 = mock_external_dependencies

    # Mock external dependencies
    mock_extractbook.return_value = None
    mock_create_textbook_in_db.return_value = None
    mock_create_book_in_db.return_value = MagicMock(id=1, title=fake_title, uuid=fake_uuid)

    # Simulate a file upload
    with open(temp_file_path, "rb") as temp_file:
        response = client.post(url_for('upload'), data={'file': (temp_file, 'dummy.epub')})

    # Assert that the response is a redirect to the library page
    assert response.status_code == 302
    assert response.location == url_for('library', _external=True)

    # Add more specific assertions based on the expected behavior of your application

    # Example: Assert that the flash message indicates success
    with client.session_transaction() as session:
        flash_messages = dict(session['_flashes'])
        assert 'success' in flash_messages
        assert flash_messages['success'] == f'{fake_title} uploaded successfully!'

    # Example: Assert that the mock functions were called with the correct arguments
    mock_extractbook.assert_called_once_with(MagicMock(), f'book/{fake_uuid}')
    mock_create_textbook_in_db.assert_called_once_with(MagicMock(), mock_create_book_in_db.return_value)
    mock_create_book_in_db.assert_called_once_with(MagicMock())
    mock_upload_to_s3.assert_called_once_with(aws_bucket, f'book/{fake_uuid}', f"book/{fake_uuid}/", s3)