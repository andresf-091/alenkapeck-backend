import strawberry
from typing import Optional
from uuid import UUID
from .enums import UserRole
from .errors import Validation


@strawberry.type
class User:
    id: UUID
    email: str
    username: str
    role: UserRole


@strawberry.input
class UserCreateInput:
    email: str
    username: str
    password: str
    role: UserRole = strawberry.field(default=UserRole.USER)

    def __post_init__(self):
        Validation.validate_user(self)


@strawberry.input
class UserUpdateInput:
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

    def __post_init__(self):
        Validation.validate_user(self)
