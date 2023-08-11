import xml.etree.ElementTree as ET




def retrieve_opf_location(title):
    xml_path = f'data/extracted/{title}/META-INF/container.xml'
    tree = ET.parse(xml_path)
    root = tree.getroot()
    opf_location = root.find('{urn:oasis:names:tc:opendocument:xmlns:container}rootfiles/{urn:oasis:names:tc:opendocument:xmlns:container}rootfile').attrib['full-path']
    print(opf_location) 
 
    
# def get_spine(title):
#     opf_location = get_opf_location(title)
#     spine = []
#     with open(f'data/extracted/{title}/{opf_location}', 'r', encoding='utf-8') as opf_file:
