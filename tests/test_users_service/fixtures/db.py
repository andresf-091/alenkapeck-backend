import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import NullPool
from users_service.app.models import Base, User


DATABASE_URL = "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db"


@pytest_asyncio.fixture(scope="session")
async def engine():
    eng = create_async_engine(
        DATABASE_URL,
        echo=False,
        future=True,
        poolclass=NullPool,
    )
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()


@pytest_asyncio.fixture
async def db_session(engine: AsyncEngine):
    """
    Для каждого теста:
      1. Берём новое соединение.
      2. Открываем транзакцию.
      3. Привязываем к ней AsyncSession.
      4. После теста откатываем транзакцию.
    """
    async with engine.connect() as conn:
        async_session = async_sessionmaker(
            bind=conn,
            expire_on_commit=False,
            class_=AsyncSession,
        )()
        yield async_session
        await async_session.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def drop_db(engine: AsyncEngine):
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
