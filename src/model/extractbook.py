import tkinter as tk
from tkinter import filedialog
import sys
import zipfile
# sys.path.append("..")

# root = tk.Tk()
# root.withdraw()

# book_path = filedialog.askopenfilename()

book_path = 'data/epub/upp.epub'

extract_directory = 'data/extracted'

with zipfile.ZipFile(book_path, 'r') as zip:
    zip.extractall(extract_directory)

print("File successfully unzipped!")