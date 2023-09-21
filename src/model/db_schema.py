from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Define the Book model
class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    UUID = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    cover = Column(String)
    isbn = Column(String)
    type = Column(String)  # e.g., 'textbook' or 'audiobook'

    # Relationships
    textbook = relationship('Textbook', back_populates='book', uselist=False)
    audiobook = relationship('Audiobook', back_populates='book', uselist=False)

# Define the Textbook model
class Textbook(Base):
    __tablename__ = 'textbooks'
    
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    book_index_number = Column(Integer)
    html_directory = Column(String)
    scroll_position = Column(String)

    # Relationships
    book = relationship('Book', back_populates='textbook')
    opf_folder_locations = relationship('OPFFolderLocation', back_populates='textbook')
    book_paths = relationship('BookPath', back_populates='textbook')
    hrefs = relationship('BookHTMLPath', back_populates='textbook')

# Define the Audiobook model (placeholder for now)
class Audiobook(Base):
    __tablename__ = 'audiobooks'
    
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    audio_path = Column(String)
    
    # Relationships
    book = relationship('Book', back_populates='audiobook')

# Define the OPFFolderLocation model
class OPFFolderLocation(Base):
    __tablename__ = 'opf_folder_locations'
    
    id = Column(Integer, primary_key=True)
    textbook_id = Column(Integer, ForeignKey('textbooks.book_id'))
    folder_location = Column(String)
    
    # Relationships
    textbook = relationship('Textbook', back_populates='opf_folder_locations')

# Define the BookPath model
class BookPath(Base):
    __tablename__ = 'book_paths'
    
    id = Column(Integer, primary_key=True)
    textbook_id = Column(Integer, ForeignKey('textbooks.book_id'))
    path = Column(String)
    
    # Relationships
    textbook = relationship('Textbook', back_populates='book_paths')

# Define the BookHTMLPath model
class BookHTMLPath(Base):
    __tablename__ = 'book_html_paths'
    
    id = Column(Integer, primary_key=True)
    textbook_id = Column(Integer, ForeignKey('textbooks.book_id'))
    href = Column(String)
    
    # Relationships
    textbook = relationship('Textbook', back_populates='hrefs')

if __name__ == '__main__':
    # Placeholder connection string (you'd replace this with your actual database details)
    DATABASE_URL = "postgresql://james:data0303@localhost:5432/booksync"
    engine = create_engine(DATABASE_URL)

    # Create the tables in the database
    Base.metadata.create_all(engine)
