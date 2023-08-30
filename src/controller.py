from model.book_manager import BookManager
from model.subclass_physbook import Textbook
# from model.class_book import Book
from model.extract_book import extract_book
from model.epub_validator import validate_book
from flask import Flask, render_template, request, flash, url_for, redirect, get_flashed_messages,  send_from_directory, session, abort, Blueprint
import os
import io
import shutil
from pathlib import Path

current_directory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder='', static_folder='')

class Config:
    SECRET_KEY = 'golf'


app.config.from_object(Config)

book_manager = BookManager()
books = book_manager.books

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




# @app.route("/<book_title>", methods=['GET', 'POST'])
# def read_book(book_title):
#     for index in range(len(books)):
#         if books[index].title == book_title:
#            session['active_book_index'] = index
#     session['iframe'] = f"{books[session['active_book_index']].opf_folder_location}/{books[session['active_book_index']].href[books[session['active_book_index']].book_index_number]}"
#     return render_template('/templates/base_reader.html', iframe=session['iframe'], active_book_index=session['active_book_index'])


# @app.route("/books/<UUID>", methods=['GET', 'POST'])
# def read_book_cont_scroll(UUID):
#     session["book_UUID"] = UUID
#     book = books[session["book_UUID"]]
#     current_page = f'{book.href[book.book_index_number]}'
#     infinite_scroll = f'{book.opf_folder_location}/infinite_scroll.html'
#     return render_template('/templates/base_reader_cont_scroll.html', UUID=UUID)

@app.route("/data/<UUID>", methods=['GET', 'POST'])
def read_book_cont_scroll(UUID):
    session["book_UUID"] = UUID
    book = books[session["book_UUID"]]
    current_page = f'{book.href[book.book_index_number]}'
    infinite_scroll = f'{book.opf_folder_location}/infinite_scroll.html'
    return render_template('/templates/reader.html', book=book)


@app.route('/infinite_scroll', methods=['GET','POST'])
def infinite_scroll():
    book = books[session["book_UUID"]]
    # css_files = find_files('.css', book.opf_folder_location)
    # return send_from_directory(f'book[UUID].opf_folder_location', filename)
    return render_template('/templates/infinite_scroll.html', books=books)


@app.route("/current_page", methods=['GET', 'POST'])
@app.route("/current_page/<path:subpath>", methods=['GET', 'POST'])
def current_page(subpath = None):
    book = books[session["book_UUID"]]
    page = f'{book.href[book.book_index_number]}'
    directory = f'{book.opf_folder_location}'
    # if subpath != None:
    #     return send_from_directory(directory, subpath)
    # return send_from_directory(directory, page)
    # return send_from_directory(books[UUID].opf_folder_location, f"/{books[UUID].href[books[UUID].book_index_number]}")
    # if subpath != None:
    # static_page = app.send_static_file(f'{book.opf_folder_location}/{static}')
    # return static_page
    # return send_from_directory(directory, page)
    # return render_template(f'/{book.opf_folder_location}/{book.href[book.book_index_number]}')


@app.route('/load_more/<UUID>/<nav>', methods=['GET','POST'])
def load_more(UUID, nav):
        UUID = session["book_UUID"]
    # if request.args.get('last_item_id') == 'next':
    # if request.args.get('nav') == 'next':
    # if nav == 'next':
        book = books[UUID]
        if book.book_index_number < len(book.href) - 1:
            books[UUID].book_index_number += 1
            return render_template(f"{book.href[book.book_index_number]}")
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
            extract_book(uploaded_file)
            filename = os.path.splitext(uploaded_file.filename)[0]
            book = Textbook(filename)
            book_manager.add_book(book)
            flash('success', f'{book.title} uploaded successfully!')
            return redirect(url_for('library'))
    elif request.method == 'GET':
        return render_template('/templates/upload.html')

@app.route("/books/<bookname>", methods=['GET'])
def bookinfo(bookname):
    return books[bookname]


@app.errorhandler(404)
def page_not_found(error):
    return render_template('/templates/404.html'), 404

if __name__ == '__main__':
    app.run(port=8000)
