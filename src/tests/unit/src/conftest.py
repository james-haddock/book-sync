import pytest
from faker import Faker
from xml.etree.ElementTree import Element, SubElement

faker = Faker()

@pytest.fixture
def fake_opf_root_with_cover():
    opf_namespace = '{http://www.idpf.org/2007/opf}'
    dc_namespace = '{http://purl.org/dc/elements/1.1/}'

    root = Element(f'{opf_namespace}package')
    metadata = SubElement(root, f'{opf_namespace}metadata')
    title = SubElement(metadata, f'{dc_namespace}title')
    title.text = faker.sentence()

    manifest = SubElement(root, f'{opf_namespace}manifest')
    cover_image_href = faker.file_name(category='image')
    cover_image_item = SubElement(manifest, f'{opf_namespace}item', attrib={'id': 'cover-image', 'href': cover_image_href})
    return root

@pytest.fixture
def fake_opf_root_without_cover():
    opf_namespace = '{http://www.idpf.org/2007/opf}'
    dc_namespace = '{http://purl.org/dc/elements/1.1/}'

    root = Element(f'{opf_namespace}package')
    metadata = SubElement(root, f'{opf_namespace}metadata')
    title = SubElement(metadata, f'{dc_namespace}title')
    title.text = faker.sentence()
    return root

@pytest.fixture
def fake_opf_folder_location(tmp_path):
    return tmp_path

@pytest.fixture
def fake_opf_root_without_title():
    opf_namespace = '{http://www.idpf.org/2007/opf}'
    root = Element(f'{opf_namespace}package')
    SubElement(root, f'{opf_namespace}metadata')
    return root

@pytest.fixture
def fake_opf_root_without_metadata():
    opf_namespace = '{http://www.idpf.org/2007/opf}'
    root = Element(f'{opf_namespace}package')
    return root

@pytest.fixture
def fake_opf_root_without_manifest():
    opf_namespace = '{http://www.idpf.org/2007/opf}'
    dc_namespace = '{http://purl.org/dc/elements/1.1/}'

    root = Element(f'{opf_namespace}package')
    metadata = SubElement(root, f'{opf_namespace}metadata')
    title = SubElement(metadata, f'{dc_namespace}title')
    title.text = faker.sentence()
    return root

@pytest.fixture
def fake_opf_root_with_invalid_cover():
    opf_namespace = '{http://www.idpf.org/2007/opf}'
    dc_namespace = '{http://purl.org/dc/elements/1.1/}'

    root = Element(f'{opf_namespace}package')
    metadata = SubElement(root, f'{opf_namespace}metadata')
    title = SubElement(metadata, f'{dc_namespace}title')
    title.text = faker.sentence()

    manifest = SubElement(root, f'{opf_namespace}manifest')
    cover_image_item = SubElement(manifest, f'{opf_namespace}item', attrib={'id': 'cover-image', 'href': 'invalid/path/to/image.jpg'})
    return root
