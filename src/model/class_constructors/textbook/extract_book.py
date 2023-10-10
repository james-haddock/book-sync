import zipfile
import os
from flask import abort

def extractbook(epub_book, extraction_directory):
    try:
        os.makedirs(extraction_directory)
    except FileExistsError:
        return FileExistsError('File already exists')
    with zipfile.ZipFile(epub_book, 'r') as zip:
        zip.extractall(extraction_directory)
        print("File successfully unzipped")
