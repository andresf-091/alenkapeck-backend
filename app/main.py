from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.models import User
from app.routers import users
from app.database import create_db_if_not_exists, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_if_not_exists()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
