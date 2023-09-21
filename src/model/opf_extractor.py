class OpfExtractor:
    def __init__(self, root):
        self.root = root
        self.opf_namespace = '{http://www.idpf.org/2007/opf}'

    def get_spine(self):
        spine = [item.attrib['idref'] for item in self.root.findall(f'{self.opf_namespace}spine/{self.opf_namespace}itemref')]
        return spine
    
    def get_href(self, spine):
        href = []
        for idref in spine:
            for element in self.root.findall(f'{self.opf_namespace}manifest/{self.opf_namespace}item'):
                if element.attrib['id'] == idref:
                    href.append(element.attrib["href"])
        return href