from fastapi import FastAPI
from contextlib import asynccontextmanager
import strawberry
from strawberry.fastapi import GraphQLRouter

from .graphql.schema import schema
from .models import User
from .database import create_db_if_not_exists


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_if_not_exists()

    yield


app = FastAPI(lifespan=lifespan)

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def root():
    return {"message": "Hello World"}
