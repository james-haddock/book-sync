from model.subclass_physbook import Textbook
# from model.class_book import Book
from model.extract_book import extract_book
from model.epub_validator import validate_book
from flask import Flask, render_template, request, flash, url_for, redirect, get_flashed_messages,  send_from_directory
import os
import io

app = Flask(__name__)

class Config:
    SECRET_KEY = 'golf'

app.config.from_object(Config)

books = []
    # {
    #     'title': 'Book 1',
    #     'author': 'Author 1',
    #     'description': 'Description of Book 1',
    #     'cover_url': 'path_to_cover_image_1.jpg'
    # },
    # {
    #     'title': 'Book 2',
    #     'author': 'Author 2',
    #     'description': 'Description of Book 2',
    #     'cover_url': 'path_to_cover_image_2.jpg'
    # },
    # # Add more books here
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'GET':
        pass


@app.route("/register", methods=['GET', 'POST'])
def registration_form():
    return render_template('register.html')


@app.route("/library", methods=['GET'])
def library():
    return render_template('library.html', books=books)

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
        return render_template('upload.html')



@app.route("/books/<bookname>", methods=['GET'])
def bookinfo(bookname):
    return books[bookname]


# @app.route('/<filename>')
# def serve_image(filename):
#     return filename


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=8000)
