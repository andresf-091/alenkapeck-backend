import factory
from uuid import uuid4
from app.models import User
from app.graphql.types.enums import UserRole


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.Faker("user_name")
    hashed_password = factory.Faker("password")
