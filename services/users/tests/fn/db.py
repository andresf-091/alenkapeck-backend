import pytest_asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import NullPool
from alembic.config import Config
from alembic import command


@pytest_asyncio.fixture(scope="session")
async def engine():
    DATABASE_URL = str(os.getenv("DATABASE_URL"))
    eng = create_async_engine(
        DATABASE_URL,
        echo=False,
        future=True,
        poolclass=NullPool,
    )

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield eng
    await eng.dispose()


@pytest_asyncio.fixture
async def db_session(engine: AsyncEngine):
    async with engine.connect() as conn:
        trans = await conn.begin()

        async_session = async_sessionmaker(
            bind=conn,
            expire_on_commit=False,
            class_=AsyncSession,
        )()

        try:
            yield async_session
        finally:
            await async_session.rollback()
            await async_session.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def drop_db(engine: AsyncEngine):
    yield
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, "base")
    await engine.dispose()
