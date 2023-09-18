from epubcheck import EpubCheck

def validate_book(book):
    epubcheckobj = EpubCheck(book)
    return epubcheckobj.valid