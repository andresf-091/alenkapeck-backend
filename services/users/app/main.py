from fastapi import FastAPI
from contextlib import asynccontextmanager
import strawberry
from strawberry.fastapi import GraphQLRouter
import asyncio

from .graphql.schema import schema
from .models import User
from .database import create_db_if_not_exists, get_db
from .grpc.server import serve_grpc


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_if_not_exists()

    asyncio.create_task(serve_grpc())

    yield


async def get_context():
    async with get_db() as session:
        return {"db_session": session}


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI(lifespan=lifespan)

app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
def root():
    return {"message": "Hello World"}
