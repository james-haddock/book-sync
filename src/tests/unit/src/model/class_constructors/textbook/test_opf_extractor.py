import pytest
import xml.etree.ElementTree as ET
from model.class_constructors.textbook.opf_extractor import OpfExtractor


def test_OpfExtractor():
    sample_opf = """<?xml version="1.0"?>
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

    root = ET.fromstring(sample_opf)
    
    extractor = OpfExtractor(root)
    
    spine = extractor.get_spine()
    assert spine == ["item1", "item2"], "Spine extraction failed"
    
    hrefs = extractor.get_href(spine)
    assert hrefs == ["path1.xhtml", "path2.xhtml"], "Href extraction failed"