import strawberry
from strawberry.types import Info
from typing import Optional, List
from uuid import UUID
from sqlalchemy import select
from ..models import User as UserModel
from .types.user import User, UserCreateInput, UserUpdateInput
from .types.errors import Errors


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, info: Info, user_id: UUID) -> Optional[User]:
        session = info.context["db_session"]

        result = await session.execute(select(UserModel).filter_by(id=user_id))
        db_user = result.scalars().first()

        if db_user:
            return User(
                id=db_user.id,
                email=db_user.email,
                username=db_user.username,
                role=db_user.role,
            )
        raise Errors.not_found("user", "database")

    @strawberry.field
    async def users(self, info: Info) -> List[User]:
        session = info.context["db_session"]

        result = await session.execute(select(UserModel))
        db_users = result.scalars().all()

        if db_users:
            return [
                User(
                    id=db_user.id,
                    email=db_user.email,
                    username=db_user.username,
                    role=db_user.role,
                )
                for db_user in db_users
            ]
        return []


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, info: Info, input: UserCreateInput) -> Optional[User]:
        session = info.context["db_session"]

        # TODO: хэширование пароля
        hashed_password = input.password + "_hashed"

        db_user = UserModel(
            email=input.email,
            username=input.username,
            hashed_password=hashed_password,
            role=input.role,
        )

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            role=db_user.role,
        )

    @strawberry.mutation
    async def delete_user(self, info: Info, user_id: UUID) -> Optional[User]:
        session = info.context["db_session"]
        result = await session.execute(select(UserModel).filter_by(id=user_id))
        db_user = result.scalars().first()

        if not db_user:
            raise Errors.not_found("user", "database")

        await session.delete(db_user)
        await session.commit()
        return db_user

    @strawberry.mutation
    async def update_user(
        self, info: Info, user_id: UUID, input: UserUpdateInput
    ) -> Optional[User]:
        session = info.context["db_session"]
        db_user = await session.get(UserModel, user_id)

        if not db_user:
            raise Errors.not_found("user", "database")

        update_data = {k: v for k, v in input.__dict__.items() if v is not None}
        for key, value in update_data.items():
            setattr(db_user, key, value)

        if "password" in update_data:
            # TODO: хэширование пароля
            update_data["password"] = update_data["password"] + "_hashed"

        for key, value in update_data.items():
            setattr(db_user, key, value)

        await session.commit()
        await session.refresh(db_user)

        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            role=db_user.role,
        )


schema = strawberry.Schema(query=Query, mutation=Mutation)
