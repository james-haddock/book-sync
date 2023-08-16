import zipfile
import os

def extract_book(epub_book):
    extract_directory = f'static/data/extracted/{os.path.splitext(epub_book.filename)[0]}'
    os.makedirs(extract_directory)
    with zipfile.ZipFile(epub_book, 'r') as zip:
        zip.extractall(extract_directory)
        print("File successfully unzipped!")
