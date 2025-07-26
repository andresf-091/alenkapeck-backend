import strawberry
from typing import Optional
from uuid import UUID
from .scalars import Email
from .enums import UserRole


@strawberry.type
class User:
    id: UUID
    email: Email
    username: str
    role: UserRole


@strawberry.input
class UserCreateInput:
    email: Email
    username: str
    password: str
    role: UserRole = strawberry.field(default=UserRole.USER)


@strawberry.input
class UserUpdateInput:
    username: Optional[str] = None
    email: Optional[Email] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
