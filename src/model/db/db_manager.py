from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from decouple import config
import logging

class DatabaseManager:
    def __enter__(self):
        try:
            database_url = config("DATABASE_URL")
            engine = create_engine(database_url)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            return self.session
        except exc.SQLAlchemyError as e:
            logging.error(f"Error creating database session: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None: 
                self.session.rollback()
            else:
                self.session.commit()
        except exc.SQLAlchemyError as e:
            logging.error(f"Error during transaction commit/rollback: {e}")
            raise
        finally:
            self.session.close()
