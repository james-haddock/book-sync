import pytest
from .......src.model.class_constructors.textbook.book_consolidator import HtmlConsolidator
import os
from tempfile import TemporaryDirectory
from bs4 import BeautifulSoup
import shutil
import re

def test_adjust_path():
    hc = HtmlConsolidator()

    assert hc.adjust_path("/book/path", "/book/path/output", "http://example.com/style.css") == "http://example.com/style.css"

    assert hc.adjust_path("/book/path", "/book/path/output", "/absolute/path/style.css") == "/absolute/path/style.css"

    assert hc.adjust_path("/book/path/file.html", "/book/path/output.html", "style.css") == "style.css"

    assert hc.adjust_path("/book/path/file.html", "/book/path/output.html", "../sibling/style.css") == "../sibling/style.css"

    assert hc.adjust_path("/book/path/file.html", "/book/path/output.html", "child/style.css") == "child/style.css"

    assert hc.adjust_path("/book/path/deeper/file.html", "/book/path/output.html", "../../style.css") == "../style.css"

    assert hc.adjust_path("/book/another_path/file.html", "/book/path/output.html", "style.css") == "../another_path/style.css"

    assert hc.adjust_path("/book/file.html", "/book/path/output.html", "static/style.css") == "../static/style.css"
    
    
def test_generate_unique_id():
    hc = HtmlConsolidator()

    assert hc.generate_unique_id("/path/to/file.html", "123") == "file_123"

    assert hc.generate_unique_id("/path/to/file.xhtml", "456") == "file_456"

    assert hc.generate_unique_id("/path/to/file", "789") == "file_789"

    assert hc.generate_unique_id("////path////to////file.html", "000") == "file_000"

    assert hc.generate_unique_id("/path.to/file.name.with.dots.html", "111") == "file.name.with.dots_111"




def test_relative_links_resolve():
    with TemporaryDirectory() as tempdir:
        file_paths = ['0fad8c06-624c-485f-abf6-52813e095698/titlepage.xhtml', '0fad8c06-624c-485f-abf6-52813e095698/text/part0000.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0001.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0002.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0003.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0004.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0005.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0006.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0007.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0008.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0009.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0010.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0011.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0012.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0013.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0014.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0015.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0016.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0017.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0018.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0019.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0020.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0021.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0022.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0023.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0024.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0025.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0026.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0027.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0028.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0029.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0030.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0031.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0032.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0033.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0034.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0035.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0036.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0037.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0038.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0039.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0040.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0041.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0042.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0043.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0044.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0045.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0046.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0047.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0048.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0049.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0050.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0051.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0052.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0053.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_000.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_001.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_002.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_003.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_004.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_005.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_006.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_007.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_008.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_009.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_010.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0054_split_011.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0055_split_000.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0055_split_001.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0055_split_002.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0055_split_003.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0055_split_004.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0056_split_000.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0056_split_001.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0056_split_002.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0056_split_003.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0056_split_004.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0056_split_005.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0057_split_000.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0057_split_001.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0058_split_000.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0058_split_001.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0059_split_000.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0059_split_001.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0060_split_000.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0060_split_001.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0060_split_002.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0060_split_003.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0060_split_004.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0060_split_005.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0060_split_006.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0060_split_007.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0061_split_000.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0061_split_001.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0061_split_002.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0061_split_003.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0061_split_004.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0061_split_005.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0061_split_006.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0061_split_007.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0061_split_008.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0061_split_009.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0062_split_000.html', '0fad8c06-624c-485f-abf6-52813e095698/text/part0062_split_001.html']
        absolute_paths = [os.path.join(tempdir, path) for path in file_paths]
        extracted_epub_directory = os.path.join(os.path.dirname(__file__), "test_data", "0fad8c06-624c-485f-abf6-52813e095698")
        temp_epub_directory = os.path.join(tempdir, '0fad8c06-624c-485f-abf6-52813e095698')
        shutil.copytree(extracted_epub_directory, temp_epub_directory)
        temp_consolidated_file = os.path.join(tempdir, "0fad8c06-624c-485f-abf6-52813e095698/text/consolidated_test.html")
        consolidator = HtmlConsolidator()
        consolidator.consolidate_html(absolute_paths, temp_consolidated_file, '0fad8c06-624c-485f-abf6-52813e095698')

        with open(temp_consolidated_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            
        email_regex = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
            
        relative_links = []
        for tag in soup.find_all(['a', 'link', 'img', 'script']):
            href = tag.get('href')
            src = tag.get('src')
            if href and not href.startswith(("http://", "https://", "#", "mailto:")) and not email_regex.match(href):
                relative_links.append(href)
            if src and not src.startswith(("http://", "https://")):
                relative_links.append(src)

        base_path = os.path.dirname(temp_consolidated_file)
        for link in relative_links:
            abs_path = os.path.join(base_path, link)
            assert os.path.exists(abs_path), f"Link {link} does not resolve to an actual file"


