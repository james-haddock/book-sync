from epubcheck import EpubCheck
from src.logger import logger

def validate_book(book):
    try:
        epubcheckobj = EpubCheck(book)

        if epubcheckobj.valid:
            logger.info(f"EPUB validation passed for {book}.")
            return True
        else:
            logger.error(f"EPUB validation failed for {book}.")
            raise Exception('Invalid EPUB file')
    except Exception as e:
        logger.exception(f"An error occurred while validating {book}: {e}")
        raise
