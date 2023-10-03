import zipfile
import os
from flask import abort

def extractbook(epub_book, UUID):
    extract_directory = f'book/{UUID}'
    try:
        os.makedirs(extract_directory)
    except FileExistsError:
        return FileExistsError('file already exists!!!')
    with zipfile.ZipFile(epub_book, 'r') as zip:
        zip.extractall(extract_directory)
        print("File successfully unzipped")
