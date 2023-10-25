from flask import Flask, render_template, request, flash, url_for, redirect, get_flashed_messages, session, jsonify
import os
import io
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
from model.db.crud import crud_book
from model.db.db_manager import DatabaseManager

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




@app.route('/book/<UUID>')
def book(UUID):
    with DatabaseManager() as session:
        book_data = crud_book.get_book_with_details(session, UUID)
        textbook = book_data['DBTextbook']
        return render_template(textbook.book_content)


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
        return render_template('/templates/library.html', books=all_books)



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
            except Exception as e:
                flash('error', f'Failed to create and add Ebook: {e}')
            return redirect(url_for('library'))
            flash('success', f'{book.title} uploaded successfully!')
            return redirect(url_for('library'))
    elif request.method == 'GET':
        return render_template('/templates/upload.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('/templates/404.html'), 404


if __name__ == '__main__':
    app.run(port=8000)         
