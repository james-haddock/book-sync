from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    database_url = "postgresql://james:data0303@localhost:5432/booksync"
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)

    def __enter__(self):
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None: 
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
