import pytest
from sqlalchemy import text
from users_service.app.models import Base
from users_service.app.graphql.types.enums import UserRole


@pytest.mark.asyncio
async def test_db_connection(db_session):
    # Проверка подключения
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


@pytest.mark.asyncio
async def test_create_and_query(db_session):
    from users_service.app.models import User

    # Создаём тестового пользователя
    new_user = User(
        email="test@gmail.com",
        username="testusername",
        hashed_password="testpassword",
    )

    db_session.add(new_user)
    await db_session.commit()

    # Проверяем, что объект сохранён
    assert new_user.id is not None

    # Получаем пользователя
    user = await db_session.get(User, new_user.id)
    assert user.email == "test@gmail.com"
    assert user.username == "testusername"
