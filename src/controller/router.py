from flask import Flask, render_template, request

app = Flask(__name__, template_folder='/view/templates/')
# book_path = '/data/epub/'

@app.route("/")
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save('/data/epub/' + uploaded_file.filename)
        return 'File uploaded successfully!'
    return 'No file uploaded.'

if __name__ == '__main__':
    app.run(port=5000)

    