import factory
import uuid
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from users_service.app.main import app
from users_service.app.database import get_db
from users_service.app.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.Faker("user_name")
    hashed_password = factory.Faker("password")
