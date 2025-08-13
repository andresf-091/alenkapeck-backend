from typing import Optional, Sequence
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User as UserModel


async def get_user(session: AsyncSession, user_id: UUID) -> Optional[UserModel]:
    result = await session.execute(select(UserModel).filter_by(id=user_id))
    return result.scalars().first()


async def get_users(session: AsyncSession) -> Sequence[UserModel]:
    result = await session.execute(select(UserModel))
    return result.scalars().all()


async def create_user(
    session: AsyncSession, email: str, username: str, password: str, role: str
) -> UserModel:
    hashed_password = password + "_hashed"  # TODO: хэширование

    db_user = UserModel(
        email=email,
        username=username,
        hashed_password=hashed_password,
        role=role,
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


async def delete_user(session: AsyncSession, user_id: UUID) -> Optional[UserModel]:
    user = await get_user(session, user_id)
    if user:
        await session.delete(user)
        await session.commit()
    return user


async def update_user(
    session: AsyncSession, user_id: UUID, **kwargs
) -> Optional[UserModel]:
    user = await get_user(session, user_id)
    if user:
        for key, value in kwargs.items():
            if key not in user.__dict__:
                continue
            setattr(user, key, value)
        await session.commit()
        await session.refresh(user)
    return user
