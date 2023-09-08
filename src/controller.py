from model.book_manager import BookManager
from model.subclass_physbook import Textbook
# from model.class_book import Book
from model.extract_book import extract_book
from model.epub_validator import validate_book
from flask import Flask, render_template, request, flash, url_for, redirect, get_flashed_messages,  send_from_directory, session, abort, Blueprint, jsonify, send_file
import os
import io
import shutil
from pathlib import Path
import logging
import uuid
from model.book_path_corrector import update_links


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

# @app.route("/custom_static", methods=['GET', 'POST'])
# def custom_static():
#     send_from_



@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/templates/login.html')
    elif request.method == 'GET':
        pass


@app.route("/register", methods=['GET', 'POST'])
def registration_form():
    return render_template('/templates/register.html')



@app.route('/data', methods=['GET', 'POST'])
def ebook_content():
    UUID = request.args.get('UUID')
    session["book_UUID"] = UUID
    book = books[UUID]
    return render_template('/templates/reader.html', UUID=UUID, current_page=book.href[book.book_index_number], book_path=book.book_path)

@app.route('/get_url', methods=['GET'])
def get_url():
    # Use request.args to get query parameters
    action = request.args.get('action')
    UUID = request.args.get('UUID')

    # Error handling for missing or invalid parameters
    if not action or not UUID:
        return "Missing or invalid parameters", 400
    # Error handling for missing book object
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
    return jsonify({'url': url_to_load})


# @app.route('/book/<UUID>/load', methods=['GET', 'POST'])
# def load_initial_page(UUID):
#     book = books[UUID]
#     # Retrieve the saved index from the database
#     url_to_load = book.href[book.book_index_number]
#     # Get the URL to load based on the index
#     return jsonify({'url_to_load': url_to_load})



    # return render_template(f'data/{os.path.join(book.book_path, book.href[book.book_index_number])}')
    # if nav == 'load':
    #     initial_load = os.path.join(ebook_dir, book.href[book.book_index_number])
    #     return render_template(initial_load)
    # file_path = os.path.join(ebook_dir, file_path)
    # if not os.path.exists(file_path):
    #     return "File not found", 404
    # if file_path.endswith('.html'):
    #     return render_template(file_path)


# @app.route("/data/<UUID>/<nav>", methods=['GET', 'POST'])
# def read_book(UUID: str, nav=None):
#     book = books[UUID]
    # if nav == 'next' and book.book_index_number < len(book.href):
    #     book.book_index_number += 1
    #     return render_template(book.href[book.book_index_number])
    # elif nav == 'session':
    #     return render_template(book.href[book.book_index_number])
    # elif nav == 'load':
    # return render_template('/templates/reader.html', UUID=UUID, book=book)
    # else:
    #     return render_template(book.href[book.book_index_number])
    return render_template('/templates/reader.html', UUID=UUID, book=book)


# @app.route("/current_page", methods=['GET', 'POST'])
# @app.route("/current_page/<path:subpath>", methods=['GET', 'POST'])
# def current_page(subpath=None):
#     book = books[session["book_UUID"]]
#     page = f'{book.href[book.book_index_number]}'
#     directory = f'{book.opf_folder_location}'
    # if subpath != None:
    #     return send_from_directory(directory, subpath)
    # return send_from_directory(directory, page)
    # return send_from_directory(books[UUID].opf_folder_location, f"/{books[UUID].href[books[UUID].book_index_number]}")
    # if subpath != None:
    # static_page = app.send_static_file(f'{book.opf_folder_location}/{static}')
    # return static_page
    # return send_from_directory(directory, page)
    # return render_template(f'/{book.opf_folder_location}/{book.href[book.book_index_number]}')


# @app.route('/load_more/<UUID>/<nav>', methods=['GET', 'POST'])
# def load_more(UUID, nav):
#     UUID = session["book_UUID"]
#     # if request.args.get('last_item_id') == 'next':
#     # if request.args.get('nav') == 'next':
#     # if nav == 'next':
#     book = books[UUID]
#     if book.book_index_number < len(book.href) - 1:
#         books[UUID].book_index_number += 1
#         return render_template(f"{book.href[book.book_index_number]}")
    #     elif request.args.get('last_item_id') == 'previous':
    #         if books[session['active_book_index']].book_index_number > 0:
    #             books[session['active_book_index']].book_index_number -= 1
    #             return render_template(f"{books[session['active_book_index']].opf_folder_location}/{books[session['active_book_index']].href[books[session['active_book_index']].book_index_number]}")


# @app.route("/nav/<navigation>", methods=['GET', 'POST'])
# def read_book_nav(navigation):
#     if navigation == 'next':
#         books[session['active_book_index']].book_index_number += 1
#     elif navigation == 'prev':
#         if books[session['active_book_index']].book_index_number > 0:
#             books[session['active_book_index']].book_index_number -= 1
#     return redirect(url_for('read_book', book_title=books[session['active_book_index']].title))
    # return render_template('/templates/base_reader.html', iframe=session['iframe'], active_book_index=session['active_book_index'])


@app.route("/library", methods=['GET'])
def library():
    return render_template('/templates/library.html', books=books)


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            book_instance_id = str(uuid.uuid4())
            extract_book(uploaded_file, book_instance_id)
            filename = os.path.splitext(uploaded_file.filename)[0]
            book = Textbook(book_instance_id)
            book_manager.add_book(book)
            flash('success', f'{book.title} uploaded successfully!')
            return redirect(url_for('library'))
    elif request.method == 'GET':
        return render_template('/templates/upload.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('/templates/404.html'), 404


if __name__ == '__main__':
    app.run(port=8000)
