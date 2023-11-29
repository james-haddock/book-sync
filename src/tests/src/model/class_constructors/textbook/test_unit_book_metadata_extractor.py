import pytest
import os
from faker import Faker
from xml.etree.ElementTree import Element, SubElement
from src.model.class_constructors.textbook.book_metadata_extractor import BookMetadataExtractor

faker = Faker()
OPF_NAMESPACE = '{http://www.idpf.org/2007/opf}'
DC_NAMESPACE = '{http://purl.org/dc/elements/1.1/}'

def test_get_title(fake_opf_root_with_cover):
    extractor = BookMetadataExtractor(fake_opf_root_with_cover, '')
    title = extractor.get_title()
    assert title is not None
    assert isinstance(title, str)

def test_get_cover_with_valid_cover(fake_opf_root_with_cover, fake_opf_folder_location):
    extractor = BookMetadataExtractor(fake_opf_root_with_cover, fake_opf_folder_location)
    cover = extractor.get_cover()
    assert cover is not None
    assert any(cover.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico', '.svg', '.tiff', '.webp'])


def test_get_cover_with_no_cover(fake_opf_root_without_cover, fake_opf_folder_location):
    extractor = BookMetadataExtractor(fake_opf_root_without_cover, fake_opf_folder_location)
    cover = extractor.get_cover()
    assert cover == 'static/Book-icon.png'

def test_get_title_with_missing_title(fake_opf_root_without_title):
    extractor = BookMetadataExtractor(fake_opf_root_without_title, '')
    title = extractor.get_title()
    assert title is None

def test_get_metadata_with_no_metadata_section(fake_opf_root_without_metadata):
    extractor = BookMetadataExtractor(fake_opf_root_without_metadata, '')
    title = extractor.get_title()
    cover = extractor.get_cover()
    assert title is None
    assert cover == 'static/Book-icon.png' 

def test_get_cover_with_no_manifest_section(fake_opf_root_without_manifest):
    extractor = BookMetadataExtractor(fake_opf_root_without_manifest, '')
    cover = extractor.get_cover()
    assert cover == 'static/Book-icon.png'
    
def test_get_cover_with_meta_element(fake_opf_root_with_meta_cover, fake_opf_folder_location):
    extractor = BookMetadataExtractor(fake_opf_root_with_meta_cover, fake_opf_folder_location)
    cover = extractor.get_cover()
    assert cover is not None
    assert any(cover.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico', '.svg', '.tiff', '.webp'])

@pytest.fixture
def fake_opf_root_with_meta_cover():
    root = Element(f'{OPF_NAMESPACE}package')
    metadata = SubElement(root, f'{OPF_NAMESPACE}metadata')
    title = SubElement(metadata, f'{DC_NAMESPACE}title')
    title.text = faker.sentence()

    meta = SubElement(metadata, f'{OPF_NAMESPACE}meta', attrib={'name': 'cover', 'content': 'cover-image-id'})
    manifest = SubElement(root, f'{OPF_NAMESPACE}manifest')
    cover_image_href = faker.file_name(category='image')
    cover_image_item = SubElement(manifest, f'{OPF_NAMESPACE}item', attrib={'id': 'cover-image-id', 'href': cover_image_href})
    return root

@pytest.fixture
def fake_opf_root_with_cover():
    root = Element(f'{OPF_NAMESPACE}package')
    metadata = SubElement(root, f'{OPF_NAMESPACE}metadata')
    title = SubElement(metadata, f'{DC_NAMESPACE}title')
    title.text = faker.sentence()

    manifest = SubElement(root, f'{OPF_NAMESPACE}manifest')
    cover_image_href = faker.file_name(category='image')
    cover_image_item = SubElement(manifest, f'{OPF_NAMESPACE}item', attrib={'id': 'cover-image', 'href': cover_image_href})
    return root

@pytest.fixture
def fake_opf_root_without_cover():
    root = Element(f'{OPF_NAMESPACE}package')
    metadata = SubElement(root, f'{OPF_NAMESPACE}metadata')
    title = SubElement(metadata, f'{DC_NAMESPACE}title')
    title.text = faker.sentence()
    return root

@pytest.fixture
def fake_opf_folder_location(tmp_path):
    return tmp_path

@pytest.fixture
def fake_opf_root_without_title():
    root = Element(f'{OPF_NAMESPACE}package')
    SubElement(root, f'{OPF_NAMESPACE}metadata')
    return root

@pytest.fixture
def fake_opf_root_without_metadata():
    root = Element(f'{OPF_NAMESPACE}package')
    return root

@pytest.fixture
def fake_opf_root_without_manifest():
    root = Element(f'{OPF_NAMESPACE}package')
    metadata = SubElement(root, f'{OPF_NAMESPACE}metadata')
    title = SubElement(metadata, f'{DC_NAMESPACE}title')
    title.text = faker.sentence()
    return root

@pytest.fixture
def fake_opf_root_that_raises_exception():
    class FakeRoot:
        def findall(self, _):
            raise Exception("Test Exception")

    return FakeRoot()

def test_get_cover_exception_handling(fake_opf_root_that_raises_exception, fake_opf_folder_location, caplog):
    extractor = BookMetadataExtractor(fake_opf_root_that_raises_exception, fake_opf_folder_location)
    cover = extractor.get_cover()
    assert cover == 'static/Book-icon.png'
    assert "Error: Could not extract cover location from XML. Using placeholder" in caplog.text