import xml.etree.ElementTree as ET

def get_opf_location(title):
    xml_path = f'data/extracted/{title}/META-INF/container.xml'
    namespace = '{urn:oasis:names:tc:opendocument:xmlns:container}'
    root = parse_and_get_root_xml(xml_path)
    opf_location = root.find(f'{namespace}rootfiles/{namespace}rootfile').attrib['full-path']
    return opf_location
    
def get_spine(title):
    spine = []
    opf_location = get_opf_location(title)
    namespace = "{http://www.idpf.org/2007/opf}"
    xml_path = f'data/extracted/{title}/{opf_location}'
    root = parse_and_get_root_xml(xml_path)
    for item in root.findall(f'{namespace}spine/{namespace}itemref'):
        spine.append(item.attrib['idref'])
    return spine

def parse_and_get_root_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return root

book = 'Refactoring Improving the Design of Existing Code (Martin Fowler)'

print(get_spine(book))