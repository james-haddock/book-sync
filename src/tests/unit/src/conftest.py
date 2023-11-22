import pytest
from flask.testing import FlaskClient
from faker import Faker
from factory import Factory, LazyAttribute
from ....controller import app as flask_app
from ....model.db.db_manager import DatabaseManager
from ....model.class_constructors.textbook import class_textbook, extract_book
from ....model.db.crud import crud_book, crud_textbook, s3_crud
import uuid

fake = Faker()

class BookFactory(Factory):
    class Meta:
        model = class_textbook.Textbook

    title = LazyAttribute(lambda _: fake.text(max_nb_chars=50))
    uuid = LazyAttribute(lambda _: str(uuid.uuid4()))

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    yield flask_app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def session(app):
    with app.app_context():
        # You may not need to explicitly create tables here if DatabaseManager handles it
        pass

    with app.test_request_context():
        with DatabaseManager() as session:
            yield session

    # You may not need to explicitly drop tables here if DatabaseManager handles it

@pytest.fixture
def book_factory():
    return BookFactory

@pytest.fixture
def mock_external_dependencies(book_factory, mocker):
    mocker.patch('ABReader.src.controller.extract_book.extractbook')
    mocker.patch('ABReader.src.model.db.crud_book.create_book_in_db')
    mocker.patch('ABReader.src.model.db.crud_textbook.create_textbook_in_db')
    mocker.patch('ABReader.src.controller.s3_crud.upload_to_s3')

    mock_extractbook = extract_book.extractbook
    mock_create_textbook_in_db = crud_textbook.create_textbook_in_db
    mock_create_book_in_db = crud_book.create_book_in_db
    mock_upload_to_s3 = s3_crud.upload_to_s3

    return mock_extractbook, mock_create_textbook_in_db, mock_create_book_in_db, mock_upload_to_s3
