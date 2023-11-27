import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.model.db.db_schema.db_schema import Base 

@pytest.fixture(scope="function")
def db_session(postgresql):
    engine = create_engine(postgresql.url())
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
