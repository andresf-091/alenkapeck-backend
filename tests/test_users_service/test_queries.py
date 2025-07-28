import pytest

from .fixtures.data_factories import UserFactory


@pytest.mark.asyncio
async def test_get_user(async_client, db_session):
    test_user = UserFactory()

    db_session.add(test_user)
    await db_session.commit()

    assert test_user.id is not None

    query = """
        query GetUser($userId: UUID!) {
            user(userId: $userId) {
                id
                email
                username
                role
            }
        }
    """

    variables = {"userId": str(test_user.id)}

    response = await async_client.post(
        "/graphql",
        json={"query": query, "variables": variables},
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["user"]["id"] == str(test_user.id)
    assert data["data"]["user"]["email"] == test_user.email
    assert data["data"]["user"]["username"] == test_user.username
    assert data["data"]["user"]["role"] == test_user.role.name
