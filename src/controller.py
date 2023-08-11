from model.subclass_physbook import Physbook
from model.class_book import Book
from model.extract_book import extract_book
from model.epub_validator import validate_book
from flask import Flask, render_template, request
import os
import io

app = Flask(__name__)

books = {}

@app.route("/")
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        extract_book(uploaded_file)
        filename = os.path.splitext(uploaded_file.filename)[0]
        books[filename] = Physbook(filename)
        # return f'File {books[filename].filename} uploaded successfully!'
        return f'{books[filename].href}'


# @app.route("/book/<bookname>", methods=['GET'])
# def index(bookname):
#     return books[bookname]

if __name__ == '__main__':
    app.run(port=8000)
