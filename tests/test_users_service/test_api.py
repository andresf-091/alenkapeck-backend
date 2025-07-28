import pytest


@pytest.mark.asyncio
async def test_api_isready(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_graphql_endpoint(async_client):
    response = await async_client.get("/graphql")
    assert response.status_code == 200
