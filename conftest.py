import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.model.db.db_schema.db_schema import Base

# @pytest.fixture(scope="function")
# def db_session(postgresql):
#     user = postgresql.info.user
#     password = postgresql.info.password
#     dbname = postgresql.info.dbname
#     host = postgresql.info.host
#     port = postgresql.info.port

#     url = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

#     engine = create_engine(url)
#     Base.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     yield session
#     session.close()
#     Base.metadata.drop_all(engine)

@pytest.fixture
def db_url(postgresql):
    user = postgresql.info.user
    password = postgresql.info.password
    dbname = postgresql.info.dbname
    host = postgresql.info.host
    port = postgresql.info.port

    url = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    return url