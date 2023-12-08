import pytest
from unittest.mock import patch, MagicMock, mock_open, Mock, PropertyMock
import uuid
from src.model.class_constructors.textbook.textbook_initialiser import TextbookInitialiser, logger
from faker import Faker
import logging

faker = Faker()

@pytest.fixture
def mock_uuid():
    return uuid.uuid4()

@pytest.fixture
def textbook_initialiser_get_opf_location(mocker):
    mock_get_opf_location = mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.TextbookInitialiser.get_opf_location')
    mock_get_opf_location.return_value = 'route/to/opf/file.opf'
    return mock_get_opf_location
    
@pytest.fixture
def os_path_dirname(mocker):
    mock_os_path_dirname = mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.os.path.dirname')
    mock_os_path_dirname.return_value = 'route/to/opf'
    return mock_os_path_dirname

@pytest.fixture
def opf_extractor(mocker):
    mock_opf_extractor = mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.OpfExtractor')
    mock_opf_extractor_instance = Mock()
    mock_opf_extractor_instance.get_spine.return_value = ["item1", "item2", "item3"]
    mock_opf_extractor_instance.get_href.return_value = ["path1.xhtml", "path2.xhtml", "path3.xhtml"]
    mock_opf_extractor.return_value = mock_opf_extractor_instance
    return mock_opf_extractor_instance
    
@pytest.fixture
def book_metadata_extractor(mocker):
    mock_book_metadata_extractor = mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.BookMetadataExtractor')
    mock_book_metadata_extractor_instance = Mock()
    mock_book_metadata_extractor_instance.get_title.return_value = faker.text(max_nb_chars=20)
    mock_book_metadata_extractor_instance.get_cover.return_value = faker.file_path(depth=3, category='image')
    mock_book_metadata_extractor.return_value = mock_book_metadata_extractor_instance
    return mock_book_metadata_extractor_instance
    
@pytest.fixture
def html_consolidation_manager(mocker):
    mock_html_consolidation_manager = mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.HtmlConsolidationManager')
    mock_html_consolidation_manager_instance = Mock()
    mock_html_consolidation_manager_instance.consolidate_html_files.return_value = 'consolidate'
    mock_html_consolidation_manager.return_value = mock_html_consolidation_manager
    return mock_html_consolidation_manager
    
@pytest.fixture
def mock_xml_parser(mocker):
    mock_parser = MagicMock()
    mock_root = MagicMock()
    mock_element = MagicMock()
    mock_element.attrib = {'full-path': 'route/to/opf/file.opf'}
    mock_root.find.return_value = mock_element
    mock_parser.get_root.return_value = mock_root
    mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.XmlParser', return_value=mock_parser)
    return mock_parser, mock_root

@pytest.mark.unit
def test_textbook_initialiser(mock_uuid, mock_xml_parser, textbook_initialiser_get_opf_location,
                              os_path_dirname, opf_extractor, book_metadata_extractor,
                              html_consolidation_manager):
    mock_parser, mock_root = mock_xml_parser

    textbook_initialiser = TextbookInitialiser(mock_uuid)
    assert textbook_initialiser.container_namespace == '{urn:oasis:names:tc:opendocument:xmlns:container}'
    assert textbook_initialiser.container_path == f'src/book/{mock_uuid}/META-INF/container.xml'
    assert textbook_initialiser.container_root == mock_root
    assert textbook_initialiser.opf == textbook_initialiser_get_opf_location()
    assert textbook_initialiser.opf_path == f'src/book/{mock_uuid}/{textbook_initialiser.opf}'
    assert textbook_initialiser.opf_folder_location == 'route/to/opf'
    assert textbook_initialiser.opf_root == mock_root 
    assert textbook_initialiser.spine == ["item1", "item2", "item3"]
    assert textbook_initialiser.href == ["path1.xhtml", "path2.xhtml", "path3.xhtml"]
    assert textbook_initialiser.title == book_metadata_extractor.get_title()

@pytest.mark.unit
def test_get_opf_location_attribute_error(mock_uuid, mock_xml_parser, caplog):
    mock_parser, mock_root = mock_xml_parser
    mock_root.find.side_effect = AttributeError()
    textbook_initialiser = TextbookInitialiser(mock_uuid)
    assert textbook_initialiser.opf is None
    assert "Error: Could not find the attribute 'full-path' in XML." in caplog.text

@pytest.mark.unit
def test_get_opf_location_exception(mock_uuid, mock_xml_parser):
    mock_parser, mock_root = mock_xml_parser
    mock_root.find.side_effect = Exception("General error")
    with pytest.raises(Exception) as exc_info:
        TextbookInitialiser(mock_uuid)
    assert str(exc_info.value) == "General error"
