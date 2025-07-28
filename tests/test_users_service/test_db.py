import pytest
from sqlalchemy import select, text
from sqlalchemy.exc import DBAPIError

from users_service.app.models import User
from .fixtures.data_factories import UserFactory


@pytest.mark.asyncio
async def test_db_connection(db_session):
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1


@pytest.mark.asyncio
async def test_create_and_query(db_session):
    good_user = UserFactory(username="testusername", email="test@gmail.com")

    db_session.add(good_user)
    await db_session.commit()

    assert good_user.id is not None

    user = await db_session.get(User, good_user.id)

    assert user.email == "test@gmail.com"
    assert user.username == "testusername"


@pytest.mark.asyncio
async def test_create_and_query_wrong(db_session):
    bad_user = UserFactory(id=1234567890)

    db_session.add(bad_user)
    with pytest.raises(DBAPIError):
        await db_session.commit()

    await db_session.rollback()

    result = await db_session.execute(
        select(User).where(User.username == bad_user.username)
    )
    assert result.scalars().first() is None
