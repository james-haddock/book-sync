from model.subclass_physbook import Textbook
# from model.class_book import Book
from model.extract_book import extract_book
from model.epub_validator import validate_book
from flask import Flask, render_template, request
import os
import io

app = Flask(__name__)

books = {}

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        extract_book(uploaded_file)
        filename = os.path.splitext(uploaded_file.filename)[0]
        books[filename] = Textbook(filename)
        # return f'File {books[filename].filename} uploaded successfully!'
        return f'{books[filename].href}'

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'GET':
        pass


@app.route("/register", methods=['GET', 'POST'])
def registration_form():
    return render_template('register.html')


@app.route("/books", methods=['GET'])
def book_index():
    return render_template('book_index.html')

@app.route("/upload", methods=['GET'])
def uploadform():
    return render_template('upload.html')

@app.route("/books/<bookname>", methods=['GET'])
def bookinfo(bookname):
    return books[bookname]

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=8000)
