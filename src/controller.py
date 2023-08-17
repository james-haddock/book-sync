from model.subclass_physbook import Textbook
# from model.class_book import Book
from model.extract_book import extract_book
from model.epub_validator import validate_book
from flask import Flask, render_template, request, flash, url_for, redirect, get_flashed_messages,  send_from_directory, session
import os
import io

app = Flask(__name__, template_folder='', static_folder='')


class Config:
    SECRET_KEY = 'golf'


app.config.from_object(Config)

books = []


@app.route("/")
def index():
    return render_template('/templates/index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/templates/login.html')
    elif request.method == 'GET':
        pass

# @app.route("/select_book/<book_title>", methods=['GET', 'POST'])
# def select_book(book_title):
#     title_index = books.index(book_title)


@app.route("/iframe", methods=['GET', 'POST'])
def iframe():
    return render_template(session['iframe'])


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


@app.route("/<book_title>", methods=['GET', 'POST'])
def read_book_cont_scroll(book_title):
    for index in range(len(books)):
        if books[index].title == book_title:
            session['active_book_index'] = index
    session['iframe'] = f"{books[session['active_book_index']].opf_folder_location}/{books[session['active_book_index']].href[books[session['active_book_index']].book_index_number]}"
    return render_template('/templates/base_reader_cont_scroll.html', iframe=session['iframe'], active_book=session['active_book_index'])


@app.route("/nav/<navigation>", methods=['GET', 'POST'])
def read_book_nav(navigation):
    if navigation == 'next':
        books[session['active_book_index']].book_index_number += 1
    elif navigation == 'prev':
        if books[session['active_book_index']].book_index_number > 0:
            books[session['active_book_index']].book_index_number -= 1
    return redirect(url_for('read_book', book_title=books[session['active_book_index']].title))
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
            books.append(Textbook(filename))
            flash('success', f'{filename} uploaded successfully!')
            return redirect(url_for('library'))
    elif request.method == 'GET':
        return render_template('/templates/upload.html')


@app.route('/load_more', methods=['GET'])
def load_more():
    if request.args.get('last_item_id') == 'next':
        if books[session['active_book_index']].book_index_number < len(books[session['active_book_index']].href) - 1:
            books[session['active_book_index']].book_index_number += 1
            return render_template(f"{books[session['active_book_index']].opf_folder_location}/{books[session['active_book_index']].href[books[session['active_book_index']].book_index_number]}")
    elif request.args.get('last_item_id') == 'next':
        if books[session['active_book_index']].book_index_number < len(books[session['active_book_index']].href) - 1:
            books[session['active_book_index']].book_index_number += 1
            return render_template(f"{books[session['active_book_index']].opf_folder_location}/{books[session['active_book_index']].href[books[session['active_book_index']].book_index_number]}")
        

@app.route("/books/<bookname>", methods=['GET'])
def bookinfo(bookname):
    return books[bookname]


@app.errorhandler(404)
def page_not_found(error):
    return render_template('/templates/404.html'), 404


if __name__ == '__main__':
    app.run(port=8000)
