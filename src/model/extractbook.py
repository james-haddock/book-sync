import zipfile

def extract_book(epub_book):
    extract_directory = 'data/extracted'
    with zipfile.ZipFile(epub_book, 'r') as zip:
        zip.extractall(extract_directory)
        print("File successfully unzipped!")
