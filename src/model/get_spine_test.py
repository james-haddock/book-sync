import pytest
from get_spine import get_opf_location, retrieve_opf_parser



def test_retrieve_opf():
    book_title = 'Refactoring Improving the Design of Existing Code (Martin Fowler)'
    assert get_opf_location(book_title) == "OEBPS/xhtml/9780134757704.opf"

def test_retrieve_opf_parser():
    book_title = 'Refactoring Improving the Design of Existing Code (Martin Fowler)'
    assert retrieve_opf_parser(book_title) == "OEBPS/xhtml/9780134757704.opf"