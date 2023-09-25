from model.book_manager import BookManager
from model.subclass_physbook import Textbook
from model.class_book import Book
from model.xml_parser import XmlParser
from model.book_consolidator import HtmlConsolidator
from model.html_consolidation_manager import HtmlConsolidationManager
from model.opf_extractor import OpfExtractor
from model.book_metadata_extractor import BookMetadataExtractor
from model.extract_book import extract_book
from model.epub_validator import validate_book
from flask import Flask, render_template, request, flash, url_for, redirect, get_flashed_messages,  send_from_directory, session, abort, Blueprint, jsonify, send_file
import os
import io
import shutil
from pathlib import Path
import logging
import uuid
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import Session, sessionmaker
from model.db_manager import DatabaseManager



def has_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].isalpha()


current_directory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder='', static_folder='')


class Config:
    SECRET_KEY = 'golf'


app.config.from_object(Config)

book_manager = BookManager()
books = book_manager.books

logger = app.logger
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s: %(message)s"))

logger.addHandler(console_handler)


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
    return render_template('/templates/register.html')




@app.route('/book/<UUID>')
def book(UUID):
    book = books[UUID]
    current_page = os.path.join(book.book_path, book.href[book.book_index_number])
    html_directory = os.path.dirname(current_page) + "/"
    return render_template('templates/reader.html', UUID=UUID, base=html_directory[5:], book_title=book.title)



@app.route('/get_content', methods=['GET'])
def get_content():
    action = request.args.get('action')
    UUID = request.args.get('UUID')
    if not action or not UUID:
        return "Missing or invalid parameters", 400
    if UUID not in books:
        return "Book not found", 404
    current_book = books[UUID]
    current_position = current_book.book_index_number
    max_position = len(current_book.href) - 1

    if action == 'initial':
        url_to_load = current_book.href[current_position]
    elif action == 'next':
        current_position = min(current_position + 1, max_position)
    elif action == 'prev':
        current_position = max(0, current_position - 1)

    current_book.book_index_number = current_position
    url_to_load = current_book.href[current_position]
    return render_template(current_book.book_path + '/' + url_to_load)


@app.route("/library", methods=['GET'])
def library():
    db_manager = DatabaseManager()
    books = db_manager.load_books_with_details()
    return render_template('/templates/library.html', books=books)


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            book_instance_id = str(uuid.uuid4())
            extract_book(uploaded_file, book_instance_id)
            
            db_manager = DatabaseManager()
            
            try:
                textbook = Textbook(book_instance_id)
                db_manager.add_textbook(textbook)
            except Exception as e:
                flash('error', f'Failed to create and add Textbook: {e}')
                return redirect(url_for('library'))
                
            try:
                book = Book(book_instance_id)
                book.add_textbook(textbook)
                db_manager.add_book(book)
            except Exception as e:
                flash('error', f'Failed to create and add Book: {e}')
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
