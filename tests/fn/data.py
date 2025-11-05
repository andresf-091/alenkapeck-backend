import pytest_asyncio
import httpx
from uuid import UUID


@pytest_asyncio.fixture()
async def test_user():

    mutation = """
        mutation {
            createUser(input: {
                email: "test1@gmail.com",
                username: "testuser1",
                password: "testpassword"
            }) {
                id
            }
        }
    """

    async with httpx.AsyncClient() as client:

        response = await client.post(
            "http://localhost:8000/graphql",
            json={"query": mutation},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            user_id = response.json()["data"]["createUser"]["id"]

    yield user_id

    mutation = f"""
        mutation {{
            deleteUser(userId: "{user_id}") {{
                id
            }}
        }}
    """

    async with httpx.AsyncClient() as client:

        response = await client.post(
            "http://localhost:8000/graphql",
            json={"query": mutation},
            headers={"Content-Type": "application/json"},
        )
