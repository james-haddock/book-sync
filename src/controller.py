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
from model.db.crud import crud_textbook, crud_book
from model.db.db_schema import db_schema
from model.class_constructors import class_book
from model.class_constructors.textbook import (class_textbook, xml_parser, 
                                               book_consolidator, html_consolidation_manager, opf_extractor,
                                               book_metadata_extractor, extract_book, epub_validator)
from bs4 import BeautifulSoup, Doctype
from model.db.crud import crud_book
from model.db.db_manager import DatabaseManager
from model.volumes.s3_crud import s3_crud
import copy
from model.change_urls_to_presigned import change_urls_to_presigned
from model.save_book_session import save_book_session_js

change_urls_to_presigned = change_urls_to_presigned()

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

def has_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].isalpha()

current_directory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder='', static_folder='')


app.config.from_object(Config)

crud_book = crud_book.CrudBook()
crud_textbook = crud_textbook.CrudTextbook()


@app.route("/")
def index():
    return render_template('/templates/index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/templates/login.html')
    elif request.method == 'GET':
        pass


@app.route("/register", methods=['GET', 'POST'])
def registration_form():
    if request.method == 'GET':
        return render_template('/templates/register.html')
#     if request.method == 'POST':
    

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
            return "Error fetching book content", 500

        amended_html = change_urls_to_presigned.change_html_links(html_content, UUID, aws_bucket, s3)
        save_book_session = save_book_session_js(UUID)
        amended_html = amended_html.replace('</head>', f'<script>{save_book_session}</script></head><style>body{{overflow-x:hidden;}}</style>')

        return render_template('templates/reader_nav.html', amended_html=amended_html, book_title=book_data['DBBook'].title)


    
    
    
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
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            UUID = str(uuid.uuid4())
            extraction_directory = f'book/{UUID}'
            extract_book.extractbook(uploaded_file, extraction_directory)
            try:
                textbook = class_textbook.Textbook(UUID)
                book = crud_book.create_book_in_db(textbook)
                crud_textbook.create_textbook_in_db(textbook, book)
                s3_crud.upload_to_s3(aws_bucket, extraction_directory, f"{extraction_directory}/", s3)
                flash('success', f'{book.title} uploaded successfully!')
            except Exception as e:
                flash('error', f'Failed to create and add Ebook: {e}')
            return redirect(url_for('library'))
    elif request.method == 'GET':
        return render_template('/templates/upload.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('/templates/404.html'), 404


if __name__ == '__main__':
    app.run(port=8000)         
