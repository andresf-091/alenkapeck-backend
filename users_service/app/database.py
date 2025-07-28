import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import asyncpg

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def get_db():
    print("ИСПОЛЬЗУЕТСЯ ОРИГИНАЛЬНАЯ ФУНКЦИЯ")
    async with AsyncSessionLocal() as session:
        yield session


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
