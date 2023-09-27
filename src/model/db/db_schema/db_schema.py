from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from .db_base import Base


class DBBook(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    UUID = Column(String, unique=True, nullable=False)
    title = Column(String)
    cover = Column(String)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='books', foreign_keys=[user_id])
    
    current_reader_id = Column(Integer, ForeignKey('users.id'))
    current_reader = relationship('User', back_populates='currently_reading', foreign_keys=[current_reader_id], uselist=False)
    
    textbook = relationship('DBTextbook', back_populates='book', uselist=False)
    audiobook = relationship('DBAudiobook', back_populates='book', uselist=False)


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


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(128))
    
    books = relationship('DBBook', back_populates='user', foreign_keys=DBBook.user_id)
    currently_reading_id = Column(Integer, ForeignKey('books.id'))
    currently_reading = relationship('DBBook', back_populates='current_reader', primaryjoin="User.id == DBBook.current_reader_id", uselist=False, post_update=True)

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class DBAudiobook(Base):
    __tablename__ = 'audiobooks'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship('DBBook', back_populates='audiobook')


if __name__ == '__main__':
    DATABASE_URL = "postgresql://james:data0303@localhost:5432/booksync"
    engine = create_engine(DATABASE_URL)
        
    Base.metadata.create_all(engine)
