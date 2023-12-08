import pytest
import xml.etree.ElementTree as ET
from src.model.class_constructors.textbook.opf_extractor import OpfExtractor, logger
import factory
from unittest.mock import patch, MagicMock

@pytest.fixture
def sample_opf():
    return """<?xml version="1.0"?>
    <package xmlns="http://www.idpf.org/2007/opf">
        <manifest>
            <item id="item1" href="path1.xhtml" />
            <item id="item2" href="path2.xhtml" />
        </manifest>
        <spine>
            <itemref idref="item1" />
            <itemref idref="item2" />
        </spine>
    </package>
    """

@pytest.mark.unit
def test_OpfExtractor(sample_opf):
    root = ET.fromstring(sample_opf)
    extractor = OpfExtractor(root)
    spine = extractor.get_spine()
    assert spine == ["item1", "item2"], "Spine extraction failed"
    hrefs = extractor.get_href(spine)
    assert hrefs == ["path1.xhtml", "path2.xhtml"], "Href extraction failed"

@pytest.mark.unit
@pytest.fixture
def extractor():
    root_mock = MagicMock()
    extractor = OpfExtractor(root_mock)
    root_mock.findall.side_effect = Exception("Forced error for testing")
    return extractor

@pytest.mark.unit
def test_get_spine_exception(extractor):
    with patch('src.model.class_constructors.textbook.opf_extractor.logger') as mock_logger:
        spine = extractor.get_spine()
        mock_logger.error.assert_called_once_with("Unexpected error while fetching spine from XML: Forced error for testing")
        assert spine == [], "Spine should be empty on exception"
        
     
@pytest.mark.unit   
def test_get_href_exception(extractor):
    with patch('src.model.class_constructors.textbook.opf_extractor.logger') as mock_logger:
        href = extractor.get_href(["item1", "item2"])
        mock_logger.error.assert_called_once_with("Unexpected error while fetching href from XML: Forced error for testing")
        assert href == [], "Spine should be empty on exception"