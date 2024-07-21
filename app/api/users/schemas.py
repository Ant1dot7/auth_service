from datetime import date

from pydantic import BaseModel, EmailStr

from domain.entities.users import User


class UserInSchema(BaseModel):
    username: str
    password: str
    email: EmailStr
    date_birth: date | None


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    date_birth: date | None
    avatar: str | None

    @classmethod
    def from_entity(cls, user: User) -> 'UserOutSchema':
        return cls(
            id=user.id,
            username=user.username.as_json(),
            email=user.email.as_json(),
            date_birth=user.date_birth,
            avatar=user.avatar,
        )
