from dataclasses import asdict
from typing import Any, Mapping

from domain.entities.users import User as UserEntity
from domain.values.users import UserName, Password, Email
from infra.db.models.users import User as UserDto


def convert_user_entity_to_dict(user: UserEntity) -> Mapping[str, Any]:
    return {
        'username': user.username.as_json(),
        'password': user.password.as_json(),
        'email': user.email.as_json(),
        'date_birth': user.date_birth,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'bio': user.bio,
        'avatar': user.avatar,
        'verify': user.verify,
        'created_at': user.created_at,
        'updated_at': user.updated_at,
    }


def convert_user_dto_to_entity(user: UserDto) -> UserEntity:
    return UserEntity(
        id=user.id,
        username=UserName(value=user.username, _need_validate=False),
        password=Password(value=user.password, need_hash=False, _need_validate=False),
        email=Email(user.email, _need_validate=False),
        date_birth=user.date_birth,
        first_name=user.first_name,
        last_name=user.last_name,
        bio=user.bio,
        avatar=user.avatar,
        verify=user.verify,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


