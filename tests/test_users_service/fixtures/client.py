import pytest_asyncio
from contextlib import asynccontextmanager
from httpx import AsyncClient, ASGITransport

from users_service.app.main import app, schema


@pytest_asyncio.fixture
async def async_client(db_session):
    app.router.routes = [
        route
        for route in app.router.routes
        if not getattr(route, "path", "").startswith("/graphql")
    ]

    async def _get_test_context():
        print("ИСПОЛЬЗУЕТСЯ ПОДМЕНЁННЫЙ КОНТЕКСТ")
        return {"db_session": db_session}

    from strawberry.fastapi import GraphQLRouter

    graphql_app = GraphQLRouter(schema, context_getter=_get_test_context)

    app.include_router(graphql_app, prefix="/graphql")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
