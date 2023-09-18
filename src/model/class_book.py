import xml.etree.ElementTree as ET
# from get_spine import get_spine
# from get_spine import get_href
# from get_spine import get_title

class Book:
    def __init__(self, filename):
        self.title = ''
        self.author = ''
        self.genre = ''

    def get_title(self):
        return self.title
    
