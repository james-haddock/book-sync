import pytest
from unittest.mock import patch, MagicMock, mock_open, Mock
import uuid
from src.model.class_constructors.textbook.textbook_initialiser import TextbookInitialiser
from faker import Faker

faker = Faker()

@pytest.fixture
def mock_uuid():
    return uuid.uuid4()

@pytest.fixture
def xml_parser(mocker):
    mock_xml_parser = mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.XmlParser')
    mock_xml_parser.xml_path = faker.file_path(depth=3, category='text', extension='xml')
    mock_container_root = Mock()
    mock_xml_parser.get_root.return_value = mock_container_root
    
@pytest.fixture
def textbook_initialiser_get_opf_location(mocker):
    mock_get_opf_location = mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.TextbookInitialiser.get_opf_location')
    mock_get_opf_location.return_value = 'route/to/opf/file.opf'
    
@pytest.fixture
def os_path_dirname(mocker):
    mock_os_path_dirname = mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.os.path.dirname')
    mock_os_path_dirname.return_value = 'route/to/opf'
    
@pytest.fixture
def opf_extractor(mocker):
    mock_opf_extractor = mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.OpfExtractor')
    mock_opf_extractor.return_value = Mock()
    mock_opf_extractor.get_spine.return_value = ["item1", "item2", "item3"]
    mock_opf_extractor.get_href.return_value = ["path1.xhtml", "path2.xhtml", "path3.xhtml"]
    
@pytest.fixture
def book_metadata_extractor(mocker):
    mock_book_metadata_extractor = mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.BookMetadataExtractor')
    mock_book_metadata_extractor.return_value = Mock()
    mock_book_metadata_extractor.get_title.return_value = faker.title(max_nb_chars=20)
    mock_book_metadata_extractor.get_cover.return_value = faker.file_path(depth=3, category='image')
    
@pytest.fixture
def html_consolidation_manager(mocker):
    mock_html_consolidation_manager = mocker.patch('src.model.class_constructors.textbook.textbook_initialiser.HtmlConsolidationManager')
    mock_html_consolidation_manager.return_value = Mock()
    # mock_html_consolidation_manager.consolidate_html_files.return_value = 