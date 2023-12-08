from src.model.class_constructors.textbook.html_consolidation_manager import HtmlConsolidationManager
from src.model.class_constructors.textbook.book_consolidator import HtmlConsolidator
from faker import Faker
import uuid
import pytest

fake = Faker()

@pytest.fixture
def instance_variables():
    mock_opf_folder_location = fake.file_path(depth=3, extension='')[:-1]
    mock_href = [fake.file_path(depth=4, category='text', extension='html') for _ in range(4)]
    mock_uuid = str(uuid.uuid4())
    return mock_opf_folder_location, mock_href, mock_uuid

@pytest.mark.unit
def test_HtmlConsolidationManager_initialisation(instance_variables):
    mock_opf_folder_location, mock_href, mock_uuid = instance_variables
    test_HtmlConsolidationManager = HtmlConsolidationManager(mock_opf_folder_location, mock_href, mock_uuid)
    assert mock_opf_folder_location == test_HtmlConsolidationManager.opf_folder_location
    assert mock_href == test_HtmlConsolidationManager.href
    assert mock_uuid == test_HtmlConsolidationManager.UUID
    
@pytest.mark.unit
def test_get_href_relative_path(instance_variables):
    mock_opf_folder_location, mock_href, mock_uuid = instance_variables
    test_HtmlConsolidationManager = HtmlConsolidationManager(mock_opf_folder_location, mock_href, mock_uuid)
    test_get_href_relative_path = test_HtmlConsolidationManager.get_href_relative_path
    assert len(test_get_href_relative_path) == 4