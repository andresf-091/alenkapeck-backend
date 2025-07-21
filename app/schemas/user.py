from pydantic import BaseModel, EmailStr, ConfigDict


class Base(BaseModel):
    email: EmailStr
    username: str


class Create(Base):
    password: str


class Response(Base):
    id: int
    model_config = ConfigDict(from_attributes=True)
