import pytest
from unittest.mock import patch, MagicMock
from src.model.class_constructors.textbook.xml_parser import XmlParser
import xml.etree.ElementTree as ET

mock_xml_content = """
<library>
    <book>
        <title>Book Title 1</title>
        <author>Author 1</author>
        <year>2001</year>
    </book>
    <book>
        <title>Book Title 2</title>
        <author>Author 2</author>
        <year>2002</year>
    </book>
    <audiobook>
        <title>Audiobook Title 1</title>
        <author>Author 2</author>
        <year>2013</year>
    </audiobook>
</library>
"""

@pytest.mark.unit
def test_get_root_success_large_xml():
    with patch('xml.etree.ElementTree.parse') as mock_parse:
        mock_tree = MagicMock()
        mock_tree.getroot.return_value = ET.fromstring(mock_xml_content)
        mock_parse.return_value = mock_tree

        xml_parser = XmlParser("valid/path/to/large/xml")
        root = xml_parser.get_root()
        assert root.tag == "library"
        assert len(root.findall('book')) == 2
        assert len(root.findall('audiobook')) == 1

@pytest.mark.unit
def test_get_root_parse_error(caplog):
    with patch('xml.etree.ElementTree.parse', side_effect=ET.ParseError("Mock parse error")):
        xml_parser = XmlParser("invalid/path/to/xml")
        root = xml_parser.get_root()
        assert root is None
        assert "Error parsing XML file at invalid/path/to/xml: Mock parse error" in caplog.text

@pytest.mark.unit
def test_get_root_file_not_found_error(caplog):
    with patch('xml.etree.ElementTree.parse', side_effect=FileNotFoundError("Mock file not found error")):
        xml_parser = XmlParser("nonexistent/path/to/xml")
        root = xml_parser.get_root()
        assert root is None
        assert "XML file not found at nonexistent/path/to/xml" in caplog.text

@pytest.mark.unit
def test_get_root_unexpected_exception(caplog):
    with patch('xml.etree.ElementTree.parse', side_effect=Exception("Mock unexpected error")):
        xml_parser = XmlParser("path/to/xml")
        root = xml_parser.get_root()
        assert root is None
        assert "Unexpected error while parsing XML file at path/to/xml: Mock unexpected error" in caplog.text