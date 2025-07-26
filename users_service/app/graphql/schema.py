import strawberry
from typing import Optional, List
from uuid import UUID
from sqlalchemy import select
from ..database import get_db
from ..models import User as UserModel
from .types.user import User, UserCreateInput, UserUpdateInput
from .types.scalars import Email


@strawberry.type
class Query:
    @strawberry.field
    async def user(self, user_id: UUID) -> Optional[User]:
        async with get_db() as session:
            result = await session.execute(select(UserModel).filter_by(id=user_id))
            db_user = result.scalars().first()
            return (
                User(
                    id=db_user.id,
                    email=db_user.email,
                    username=db_user.username,
                    role=db_user.role,
                )
                if db_user
                else None
            )

    @strawberry.field
    async def users(self) -> List[User]:
        async with get_db() as session:
            result = await session.execute(select(UserModel))
            db_users = result.scalars().all()
            return (
                [
                    User(
                        id=db_user.id,
                        email=db_user.email,
                        username=db_user.username,
                        role=db_user.role,
                    )
                    for db_user in db_users
                ]
                if db_users
                else None
            )


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(self, input: UserCreateInput) -> Optional[User]:
        # TODO: хэширование пароля
        hashed_password = input.password + "_hashed"

        async with get_db() as session:

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
    async def delete_user(self, user_id: UUID) -> Optional[User]:
        async with get_db() as session:
            result = await session.execute(select(UserModel).filter_by(id=user_id))
            db_user = result.scalars().first()

            if not db_user:
                return None

            await session.delete(db_user)
            await session.commit()
            return db_user

    @strawberry.mutation
    async def update_user(
        self, user_id: UUID, input: UserUpdateInput
    ) -> Optional[User]:
        async with get_db() as session:
            db_user = await session.get(UserModel, user_id)

            if not db_user:
                return None

            db_user.email = input.email if input.email else db_user.email
            db_user.username = input.username if input.username else db_user.username
            db_user.role = input.role if input.role else db_user.role

            if input.password:
                # TODO: хэширование пароля
                hashed_password = input.password + "_hashed"
                db_user.password = hashed_password

            await session.commit()
            await session.refresh(db_user)

            return User(
                id=db_user.id,
                email=db_user.email,
                username=db_user.username,
                role=db_user.role,
            )


schema = strawberry.Schema(query=Query, mutation=Mutation)
