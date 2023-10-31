from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
import os

class DatabaseManager:
    def __enter__(self):
        database_url = os.getenv("DATABASE_URL")
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None: 
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
