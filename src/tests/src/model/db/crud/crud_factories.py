import factory
from src.model.db.db_schema.db_schema import DBBook, Association, DBTextbook
from faker import Faker
import random

fake = Faker()

class DBBookFactory(factory.Factory):
    class Meta:
        model = DBBook

    UUID = factory.LazyFunction(lambda: fake.uuid4())
    title = factory.LazyFunction(lambda: fake.text(max_nb_chars=20))
    cover = factory.LazyFunction(lambda: fake.file_path(depth=random.randint(1, 5), category='image'))
    user_id = factory.LazyFunction(lambda: random.randint(1, 999999999))
    # user = relationship('User', back_populates='books', foreign_keys=[user_id])
    # associations = relationship('Association', back_populates='book', cascade="all, delete-orphan")
    
    
# class AssociationFactory(factory.Factory):
#     class Meta:
#         model = Association

