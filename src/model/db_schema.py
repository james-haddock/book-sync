from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base


Base = declarative_base()

class DBBook(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    UUID = Column(String, unique=True, nullable=False)
    title = Column(String)
    cover = Column(String)
    
    # Relationships
    textbook = relationship('DBTextbook', back_populates='book', uselist=False)


class DBTextbook(Base):
    __tablename__ = 'textbooks'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    title = Column(String)
    cover = Column(String)
    book_path = Column(String)
    isbn = Column(String)
    book_position = Column(Integer)
    
    book = relationship('DBBook', back_populates='textbook')


# class DBAudiobook(Base):
#     __tablename__ = 'audiobooks'
    
#     id = Column(Integer, primary_key=True)
#     book_id = Column(Integer, ForeignKey('books.id'))

#     book = relationship('DBBook', back_populates='audiobook')


DATABASE_URL = "postgresql://james:data0303@localhost:5432/booksync"
engine = create_engine(DATABASE_URL)


Base.metadata.create_all(engine)
