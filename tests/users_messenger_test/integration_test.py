import pytest
import httpx


@pytest.mark.asyncio
async def test_integration(messenger_service, users_service):

    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/graphql")
        assert response.status_code == 200

        mutation = """
            mutation {
                createUser(input: {
                    email: "test1@gmail.com",
                    username: "testuser1",
                    password: "testpassword"
                }) {
                    id
                    email
                    username
                    role
                }
            }
        """

        response = await client.post(
            "http://localhost:8000/graphql",
            json={"query": mutation},
            headers={"Content-Type": "application/json"},
        )
        print(response.json())
        assert response.status_code == 200

    pass
