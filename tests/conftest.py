import pytest_asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from users_service.app.database import Base
from users_service.app.models import user
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """Фикстура для создания event loop (решает проблему с 'different loop')."""

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_engine():
    """Фикстура для асинхронного движка SQLAlchemy."""
    engine = create_async_engine(
        "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
    )

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def setup_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Очищаем БД
        await conn.run_sync(Base.metadata.create_all)  # Создаем таблицы
    yield


@pytest_asyncio.fixture(scope="function")
async def db_session(async_engine, setup_db):
    """Фикстура для ORM-сессии с автоматическим откатом."""
    async with async_engine.connect() as conn:
        AsyncSessionLocal = async_sessionmaker(
            bind=conn, expire_on_commit=False, autoflush=False
        )
        async with AsyncSessionLocal() as session:
            yield session
            await session.rollback()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def cleanup_db_after_tests():
    engine = create_async_engine(
        "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"
    )
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
