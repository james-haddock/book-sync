from flask import Flask, render_template, request

def upload_file(upload):
    uploaded_file = request.files['file']
    if upload.filename != '':
        extract_book(uploaded_file)
        uploaded_file.save('data/epub/' + uploaded_file.filename)
        return 'File uploaded successfully!'
    return 'No file uploaded.'
