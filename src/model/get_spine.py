import xml.etree.ElementTree as ET

# def get_opf_location(title):
#     xml_path = f'data/extracted/{title}/META-INF/container.xml'
#     namespace = '{urn:oasis:names:tc:opendocument:xmlns:container}'
#     root = parse_and_get_root_xml(xml_path)
#     opf_location = root.find(f'{namespace}rootfiles/{namespace}rootfile').attrib['full-path']
#     return opf_location
    
# def get_spine_and_root(filename):
#     opf_location = get_opf_location(filename)
#     namespace = "{http://www.idpf.org/2007/opf}"
#     xml_path = f'data/extracted/{filename}/{opf_location}'
#     root = parse_and_get_root_xml(xml_path)
#     spine = [item.attrib['idref'] for item in root.findall(f'{namespace}spine/{namespace}itemref')]
#     return spine, root

# def parse_and_get_root_xml(xml_path):
#     tree = ET.parse(xml_path)
#     root = tree.getroot()
#     return root

# def get_href(filename):
#     spine, root = get_spine_and_root(filename)
#     namespace = "{http://www.idpf.org/2007/opf}"
#     href = []
#     for idref in spine:
#         for element in root.findall(f'{namespace}manifest/{namespace}item'):
#                 if element.attrib['id'] == idref:
#                      href.append(element.attrib['href'])
#     return href

# def get_title(filename):
    

# def get_author(filename):
    

# book = 'Refactoring Improving the Design of Existing Code (Martin Fowler)'

# print(get_href(book))

# class 