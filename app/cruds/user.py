from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .. import models, schemas


async def create_user(db: AsyncSession, user: schemas.user.Create) -> models.User:
    # TODO: хеширование пароля
    hashed_password = user.password + "_hashed"
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        username=user.username,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_users(db: AsyncSession) -> Sequence[models.User]:
    query = select(models.User)
    result = await db.execute(query)
    return result.scalars().all()


async def get_user(
    db: AsyncSession,
    user_id: Optional[int] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
) -> Optional[models.User]:
    query = select(models.User)
    if user_id:
        query = query.where(models.User.id == user_id)
    elif username:
        query = query.where(models.User.username == username)
    elif email:
        query = query.where(models.User.email == email)

    result = await db.execute(query)
    return result.scalars().first()


async def update_user(
    db: AsyncSession, user_id: int, user_update: schemas.user.Create
) -> Optional[models.User]:
    query = select(models.User).where(models.User.id == user_id)
    result = await db.execute(query)
    db_user = result.scalars().first()

    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
    query = select(models.User).where(models.User.id == user_id)
    result = await db.execute(query)
    db_user = result.scalars().first()

    if not db_user:
        return None

    await db.delete(db_user)
    await db.commit()
    return db_user
