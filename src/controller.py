from model.extractbook import extract_book
from flask import Flask, render_template, request
import os
import io

app = Flask(__name__)
# book_path = '/data/epub/'

@app.route("/")
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        extract_book(uploaded_file)
        return 'File uploaded successfully!'

if __name__ == '__main__':
    app.run(port=8000)

    # uploaded_file.filename