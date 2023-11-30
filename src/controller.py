from flask import Flask, render_template, request, flash, url_for, redirect, get_flashed_messages, session, jsonify, render_template_string
import os
import io
import boto3
import shutil
from pathlib import Path
import logging
import uuid
from decouple import config
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import Session, sessionmaker
from werkzeug.exceptions import HTTPException, InternalServerError, BadRequest
from src.model.db.crud import crud_textbook, crud_book
from src.model.db.db_schema import db_schema
from src.model.class_constructors import class_book
from bs4 import BeautifulSoup, Doctype
from src.model.db.crud import crud_book
from src.model.db.db_manager import DatabaseManager
from src.model.db.crud.s3_crud import s3_crud
import copy
from src.model.change_urls_to_presigned import change_urls_to_presigned
from src.model.save_book_session import save_book_session_js
from src.model.class_constructors.textbook import (class_textbook, xml_parser, 
                                               book_consolidator, html_consolidation_manager, opf_extractor,
                                               book_metadata_extractor, extract_book, epub_validator)

s3 = boto3.client(
    's3',
    aws_access_key_id=config('DO_ACCESS_KEY'),
    aws_secret_access_key=config('DO_SECRET_KEY'),
    region_name=config('DO_REGION'),
    endpoint_url=config('DO_ENDPOINT_URL')
)

aws_bucket=config('DO_BUCKET_NAME')

class Config:
    DEBUG = config("DEBUG")
    SECRET_KEY = config("FLASK_SECRET_KEY")
    DATABASE_URL = config("DATABASE_URL")
    API_KEY = config("API_KEY")

app = Flask(__name__, template_folder='', static_folder='')
app.config.from_object(Config)
crud_book = crud_book.CrudBook()
crud_textbook = crud_textbook.CrudTextbook()
change_urls_to_presigned = change_urls_to_presigned()

@app.route("/")
def index():
    return render_template('/templates/index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/templates/login.html')

@app.route("/register", methods=['GET', 'POST'])
def registration_form():
    if request.method == 'GET':
        return render_template('/templates/register.html')

def get_s3_object_content(aws_bucket, object_name, s3):
    try:
        response = s3.get_object(Bucket=aws_bucket, Key=object_name)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching S3 object {object_name}: {e}")
        return None

@app.route('/book/<UUID>')
def book(UUID):
    with DatabaseManager() as session:
        book_data = crud_book.get_book_with_details(session, UUID)
        textbook = book_data['DBTextbook']
        html_content = get_s3_object_content(aws_bucket, textbook.book_content, s3)
        if not html_content:
            raise CustomError("Error fetching book content, please try again", status_code=500)
        save_book_session = save_book_session_js(UUID)
        return render_template('templates/reader_nav.html', book_title=book_data['DBBook'].title, UUID=UUID, save_book_session=save_book_session)

@app.route('/content/<UUID>')
def content(UUID):
    with DatabaseManager() as session:
        book_data = crud_book.get_book_with_details(session, UUID)
        textbook = book_data['DBTextbook']

        html_content = get_s3_object_content(aws_bucket, textbook.book_content, s3)
        if not html_content:
            raise CustomError("Error fetching book content, please try again", status_code=500)

        amended_html = change_urls_to_presigned.change_html_links(html_content, UUID, aws_bucket, s3)
        return render_template_string(amended_html)
    
@app.route("/library", methods=['GET'])
def library():
    with DatabaseManager() as session:
        all_books = crud_book.get_all_books_with_details(session)
        all_books_copy = copy.deepcopy(all_books)
        for book in all_books_copy:
            book['DBTextbook'].cover = change_urls_to_presigned.generate_presigned_url(aws_bucket, book['DBTextbook'].cover, s3)
        return render_template('/templates/library.html', books=all_books_copy)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['file']
            if uploaded_file and '.' in uploaded_file.filename and uploaded_file.filename.rsplit('.', 1)[1].lower() == 'epub' and epub_validator(uploaded_file):
                
                try:
                    UUID = str(uuid.uuid4())
                    extraction_directory = f'src/book/{UUID}'
                    extract_book.extractbook(uploaded_file, extraction_directory)
                    textbook = class_textbook.Textbook(UUID)
                    book = crud_book.create_book_in_db(textbook)
                    crud_textbook.create_textbook_in_db(textbook, book)
                    s3_crud.upload_to_s3(aws_bucket, extraction_directory, f"{extraction_directory}/", s3)
                    flash('success', f'{book.title} uploaded successfully!')
                    return redirect(url_for('library'))
                except Exception as e:
                    app.logger.error(f'Upload Error: {e}')
                    flash('error', 'Failed to upload the book. Please try again.')
                    return render_template('/templates/upload.html'), 500
            else:
                flash('error', 'Invalid file. Only valid EPUB files are allowed.')
                return redirect(url_for('upload'))
        else:
            flash('error', 'No file selected.')
    return render_template('/templates/upload.html')

@app.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, HTTPException):
        code = error.code
        message = get_error_message(code)
    elif isinstance(error, CustomError):
        code = error.status_code
        message = error.message
    else:
        code = 500
        message = "An unexpected error has occurred."
    return render_template(f'templates/error.html', code=code, message=message), code

class CustomError(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code

def get_error_message(code):
    messages = {
        404: "Oops! The page you're looking for can't be found...",
        401: "Sorry, you need to be logged in to view this page.",
        403: "You don't have permission to access this page.",
        405: "The method you're using to request this page is not allowed.",
        408: "Your request took too long to process. Please try again.",
        500: "Something went wrong on our end. Please try again later.",
        502: "We're having trouble connecting to the server. Please try again later.",
        503: "Our service is currently unavailable due to maintenance.",
        504: "Our servers are taking longer than expected to respond."
    }
    return messages.get(code, "An unexpected error has occurred.")