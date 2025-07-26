import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncAttrs,
    async_sessionmaker,
)
import asyncpg
from contextlib import asynccontextmanager
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from sqlalchemy import func
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


@asynccontextmanager
async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_db_if_not_exists():
    try:
        conn = await asyncpg.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
    except asyncpg.exceptions.ConnectionDoesNotExistError:
        conn = await asyncpg.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database="postgres",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        await conn.execute(
            f'CREATE DATABASE "{os.getenv("POSTGRES_DB")}" OWNER "{os.getenv("POSTGRES_USER")}"'
        )
        await conn.close()
