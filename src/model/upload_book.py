# from flask import request
# from .class_constructors.textbook import extract_book

# def upload_file(upload):
#     uploaded_file = request.files['file']
#     if upload.filename != '':
#         extract_book.extractbook(uploaded_file)
#         uploaded_file.save('data/epub/' + uploaded_file.filename)
#         return 'File uploaded successfully!'
#     return 'No file uploaded.'
