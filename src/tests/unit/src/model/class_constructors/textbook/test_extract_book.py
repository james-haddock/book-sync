import pytest
import os
import shutil
from tempfile import TemporaryDirectory
from model.class_constructors.textbook.extract_book import extractbook

def test_extractbook():
    with TemporaryDirectory() as tempdir:
        test_epub_path = os.path.join(os.path.dirname(__file__), "test_data", "Clean Architecture A Craftsman’s Guide to Software Structure and Design (Martin, R.C.).epub")
        temp_epub_path = os.path.join(tempdir, "Clean Architecture A Craftsman’s Guide to Software Structure and Design (Martin, R.C.).epub")
        shutil.copy(test_epub_path, temp_epub_path)
        
        extraction_path = os.path.join(tempdir, "books/0a7e688f-d6f7-476b-80fb-e0a2078cd342")
        extractbook(temp_epub_path, extraction_path)
        
        assert os.path.exists(extraction_path), "Extraction directory should be created by extractbook"

        result = extractbook(temp_epub_path, extraction_path)
        assert isinstance(result, FileExistsError), "Should return FileExistsError if directory already exists"
        
import os

def directories_match(dir1, dir2):
    for subdir, _, filenames in os.walk(dir1):
        filenames = [f for f in filenames if f != '.DS_Store']
        rel_path = os.path.relpath(subdir, dir1)
        corresponding_subdir = os.path.join(dir2, rel_path)
        if not os.path.exists(corresponding_subdir):
            raise AssertionError(f"Directory {corresponding_subdir} missing in {dir2}")
        
        for filename in filenames:
            file1_path = os.path.join(subdir, filename)
            file2_path = os.path.join(corresponding_subdir, filename)
            
            if not os.path.exists(file2_path):
                raise AssertionError(f"File {filename} in {subdir} missing in {corresponding_subdir}")
            
            with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
                if file1.read() != file2.read():
                    raise AssertionError(f"Contents of {file1_path} and {file2_path} do not match")

    for subdir, _, _ in os.walk(dir2):
        filenames = [f for f in filenames if f != '.DS_Store']
        rel_path = os.path.relpath(subdir, dir2)
        corresponding_subdir = os.path.join(dir1, rel_path)
        if not os.path.exists(corresponding_subdir):
            raise AssertionError(f"Extra directory {subdir} found in {dir2} that's not in {dir1}")

    return True

        
        
def test_extractbook_contents_match():
    with TemporaryDirectory() as tempdir:
        test_epub_path = os.path.join(os.path.dirname(__file__), "test_data", "Clean Architecture A Craftsman’s Guide to Software Structure and Design (Martin, R.C.).epub")
        temp_epub_path = os.path.join(tempdir, "Clean Architecture A Craftsman’s Guide to Software Structure and Design (Martin, R.C.).epub")
        shutil.copy(test_epub_path, temp_epub_path)
        
        extraction_path = os.path.join(tempdir, "books/0fad8c06-624c-485f-abf6-52813e095698")
        extractbook(temp_epub_path, extraction_path)
        
        example_extract_book = os.path.join(os.path.dirname(__file__), "test_data", "0fad8c06-624c-485f-abf6-52813e095698")
        
        assert directories_match(example_extract_book, extraction_path), "Extracted contents do not match expected contents."
        
