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

s3 = boto3.client(
    's3',
    aws_access_key_id=config('DO_ACCESS_KEY'),
    aws_secret_access_key=config('DO_SECRET_KEY'),
    region_name=config('DO_REGION'),
    endpoint_url=config('DO_ENDPOINT_URL')
)

aws_bucket=config('DO_BUCKET_NAME')

database_url = config("DATABASE_URL")

class Config:
    DEBUG = config("DEBUG")
    SECRET_KEY = config("SECRET_KEY")
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




# @app.route('/book/<UUID>')
# def book(UUID):
#     with DatabaseManager() as session:
#         book_data = crud_book.get_book_with_details(session, UUID)
#         textbook = book_data['DBTextbook']
#         return render_template(textbook.book_content)
    


def generate_presigned_url(aws_bucket, object_name, s3, expiration=3600):
    try:
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': aws_bucket, 'Key': object_name},
                                                    ExpiresIn=expiration)
    except Exception as e:
        print(e)
        return None
    return response

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

        soup = BeautifulSoup(html_content, 'html.parser')
        base_s3_directory = f"book/{UUID}/"
        
        if soup.find('doctype') is None:
            soup.insert(0, Doctype('html'))

        for tag in soup.find_all('img', src=True):
            tag['src'] = generate_presigned_url_for_path(tag['src'], base_s3_directory)

        for tag in soup.find_all('a', href=True):
            if tag['href'].startswith('#'):
                continue
            if not ("://" in tag['href'] or tag['href'].startswith("/")):
                tag['href'] = generate_presigned_url_for_path(tag['href'], base_s3_directory)

        for tag in soup.find_all('link', href=True):
            if 'stylesheet' in tag.get('rel', []):
                tag['href'] = generate_presigned_url_for_path(tag['href'], base_s3_directory)

        for tag in soup.find_all('script', src=True):
            tag['src'] = generate_presigned_url_for_path(tag['src'], base_s3_directory)

        for tag in soup.find_all('image', {'xlink:href': True}):
            tag['xlink:href'] = generate_presigned_url_for_path(tag['xlink:href'], base_s3_directory)

        return render_template_string(str(soup))


def generate_presigned_url_for_path(link_path, base_s3_directory):
    if "://" in link_path:
        return link_path

    s3_key = os.path.join(base_s3_directory, link_path)
    presigned_url = generate_presigned_url(aws_bucket, s3_key, s3)

    return presigned_url if presigned_url else link_path



# @app.route('/get_content', methods=['GET'])
# def get_content():
#     with DatabaseManager() as session:
        
#         action = request.args.get('action')
#         UUID = request.args.get('UUID') 
#         if action == 'load':
#             book_data = crud_book.get_book_with_details(session, UUID)
#             textbook = book_data['DBTextbook']
#             book_content = textbook.book_content
#             with open(book_content, 'r') as file:
#                 content = file.read()
#             return jsonify({"content": content})
         




@app.route("/library", methods=['GET'])
def library():
    with DatabaseManager() as session:
        all_books = crud_book.get_all_books_with_details(session)
        all_books_copy = copy.deepcopy(all_books)
        for book in all_books_copy:
            book['DBTextbook'].cover = generate_presigned_url(aws_bucket, book['DBTextbook'].cover, s3)
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
