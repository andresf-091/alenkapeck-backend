import strawberry
from strawberry.types import Info
from typing import Optional, List
from uuid import UUID

from .. import repository as repo


from .types.user import User, UserCreateInput, UserUpdateInput, to_graphql_user
from .types.errors import Errors


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, info: Info, user_id: UUID) -> Optional[User]:
        session = info.context["db_session"]

        db_user = await repo.user.get_user(session, user_id)

        if not db_user:
            raise Errors.not_found("user", "database")

        return to_graphql_user(db_user)

    @strawberry.field
    async def users(self, info: Info) -> List[User]:
        session = info.context["db_session"]
        return [
            to_graphql_user(db_user) for db_user in await repo.user.get_users(session)
        ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, info: Info, input: UserCreateInput) -> Optional[User]:
        session = info.context["db_session"]

        db_user = await repo.user.create_user(
            session, input.email, input.username, input.password, input.role
        )

        return to_graphql_user(db_user)

    @strawberry.mutation
    async def delete_user(self, info: Info, user_id: UUID) -> Optional[User]:
        session = info.context["db_session"]

        db_user = await repo.user.delete_user(session, user_id)
        if not db_user:
            raise Errors.not_found("user", "database")

        return to_graphql_user(db_user)

    @strawberry.mutation
    async def update_user(
        self, info: Info, user_id: UUID, input: UserUpdateInput
    ) -> Optional[User]:
        session = info.context["db_session"]
        update_data = {k: v for k, v in input.__dict__.items() if v is not None}
        db_user = await repo.user.update_user(session, user_id, **update_data)

        if not db_user:
            raise Errors.not_found("user", "database")

        return to_graphql_user(db_user)


schema = strawberry.Schema(query=Query, mutation=Mutation)
