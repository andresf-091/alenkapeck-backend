from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence
from .. import schemas, cruds, models
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.user.Response)
async def create_user(
    user: schemas.user.Create, db: AsyncSession = Depends(get_db)
) -> models.User:
    return await cruds.user.create_user(db, user)


@router.get("/", response_model=Sequence[schemas.user.Response])
async def get_users(db: AsyncSession = Depends(get_db)) -> Sequence[models.User]:
    return await cruds.user.get_users(db)


@router.get("/{user_id}", response_model=schemas.user.Response)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> models.User:
    return await cruds.user.get_user(db, user_id)


@router.put("/{user_id}", response_model=schemas.user.Response)
async def update_user(
    user_id: int, user_update: schemas.user.Create, db: AsyncSession = Depends(get_db)
) -> models.User:
    return await cruds.user.update_user(db, user_id, user_update)


@router.delete("/{user_id}", response_model=schemas.user.Response)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)) -> models.User:
    return await cruds.user.delete_user(db, user_id)
