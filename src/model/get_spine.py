
def get_opf_location(title):
    with open(f'data/extracted/{title}/META-INF/container.xml', 'r', encoding='utf-8') as container:
        xml = container.read()
        speech_comma = '"'
        opf_attribute = "full-path="
        index = xml.find(opf_attribute)
        opf_location = f"{xml[index + len(opf_attribute):].split(speech_comma)[1]}"
        return opf_location