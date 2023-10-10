import pytest
from .......src.model.class_constructors.textbook.book_consolidator import HtmlConsolidator
import os
from tempfile import TemporaryDirectory

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

