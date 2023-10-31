from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from decouple import config

Base = declarative_base()


class DBBook(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    UUID = Column(String, unique=True, nullable=False)
    title = Column(String)
    cover = Column(String)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='books', foreign_keys=[user_id])
    
    current_reader_id = Column(Integer, ForeignKey('users.id'))
    current_reader = relationship('User', back_populates='currently_reading', uselist=False, foreign_keys=[current_reader_id])
    
    associations = relationship('Association', back_populates='book', cascade="all, delete-orphan")


class Association(Base):
    __tablename__ = 'associations'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    book_type = Column(String) 
    type_id = Column(Integer)  
    
    book = relationship('DBBook', back_populates='associations')


class DBTextbook(Base):
    __tablename__ = 'textbooks'
    
    id = Column(Integer, primary_key=True)
    cover = Column(String)
    book_content = Column(String)
    book_base = Column(String)
    isbn = Column(String)
    book_position = Column(Integer)


class DBAudiobook(Base):
    __tablename__ = 'audiobooks'
    
    id = Column(Integer, primary_key=True)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(128))
    
    books = relationship('DBBook', back_populates='user', foreign_keys='DBBook.user_id')
    currently_reading_id = Column(Integer, ForeignKey('books.id'))
    currently_reading = relationship('DBBook', back_populates='current_reader', uselist=False, post_update=True, foreign_keys='DBBook.current_reader_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



if __name__ == '__main__':
    DATABASE_URL = database_url = config("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
