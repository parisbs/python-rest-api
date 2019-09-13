import factory
from factory.alchemy import SQLAlchemyModelFactory

from rest_api.models import User


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    id = 1
    email = factory.Faker('email')
    name = factory.Faker('first_name')
