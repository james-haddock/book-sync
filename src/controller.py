from flask import Flask, render_template, request, flash, url_for, redirect, get_flashed_messages, session
import os
import io
import shutil
from pathlib import Path
import logging
import uuid
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import Session, sessionmaker
from model.db.db_manager import db_manager_book, db_manager_textbook
from model.class_constructors import class_book
from model.class_constructors.textbook import (class_textbook, xml_parser, 
                                               book_consolidator, html_consolidation_manager, opf_extractor,
                                               book_metadata_extractor, extract_book, epub_validator)



def has_file_extension(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].isalpha()


current_directory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder='', static_folder='')


class Config:
    SECRET_KEY = 'golf'


app.config.from_object(Config)

DATABASE_URL = "postgresql://james:data0303@localhost:5432/booksync"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

db_manager_book = db_manager_book.BookManager(session)
db_manager_textbook = db_manager_textbook.TextbookManager(session)


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
    book = db_manager_book.get_book_by_uuid(UUID)
    book_path = book.textbook.book_path
    action = request.args.get('action')
    # return render_template('templates/reader.html', UUID=UUID, base=book_path[5:], book_title=book.title)
    return render_template(book_path)


# @app.route('/get_content', methods=['GET'])
# def get_content():
#     action = request.args.get('action')
#     UUID = request.args.get('UUID')
#     if not action or not UUID:
#         return "Missing or invalid parameters", 400
#     if UUID not in books:
#         return "Book not found", 404
#     current_book = books[UUID]
#     current_position = current_book.book_index_number
#     max_position = len(current_book.href) - 1

#     if action == 'initial':
#         url_to_load = current_book.href[current_position]
#     elif action == 'next':
#         current_position = min(current_position + 1, max_position)
#     elif action == 'prev':
#         current_position = max(0, current_position - 1)

#     current_book.book_index_number = current_position
#     url_to_load = current_book.href[current_position]
#     return render_template(current_book.book_path + '/' + url_to_load)


@app.route("/library", methods=['GET'])
def library():
    books = db_manager_book.get_all_books()
    return render_template('/templates/library.html', books=books)


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            book_instance_id = str(uuid.uuid4())
            extract_book.extractbook(uploaded_file, book_instance_id)
            
        
            
            try:
                textbook = class_textbook.Textbook(book_instance_id)
                db_manager_textbook.add_textbook(textbook)
            except Exception as e:
                flash('error', f'Failed to create and add Textbook: {e}')
                return redirect(url_for('library'))
                
            try:
                book = class_book.Book(book_instance_id)
                book.add_textbook(textbook)
                db_manager_book.add_book(book)
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
