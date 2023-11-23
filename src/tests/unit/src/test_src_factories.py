import factory
from faker import Faker
fake = Faker()
from src.model.db.db_schema.db_schema import DBBook

class BookFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DBBook
    