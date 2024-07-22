from datetime import date, datetime

from pydantic import BaseModel, EmailStr

from domain.entities.users import User


class UserInSchema(BaseModel):
    username: str
    password: str
    email: EmailStr
    date_birth: date | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    date_birth: date | None
    first_name: str | None
    last_name: str | None
    bio: str | None
    verify: bool
    avatar: str | None
    created_at: datetime
    updated_at: datetime | None

    @classmethod
    def from_entity(cls, user: User) -> 'UserOutSchema':
        return cls(
            id=user.id,
            username=user.username.as_json(),
            email=user.email.as_json(),
            date_birth=user.date_birth,
            first_name=user.first_name.as_json(),
            last_name=user.last_name.as_json(),
            bio=user.bio,
            verify=user.verify,
            avatar=user.avatar,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class UserTokenOutSchema(BaseModel):
    access_token: str
    refresh_token: str


class UserUpdateSchema(BaseModel):
    date_birth: date | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
