from collections.abc import Mapping
from typing import Any

from domain.entities.users import User as UserEntity, UserRole as UserRoleEntity
from domain.values.users import (
    Email,
    Name,
    Password,
    UserName,
)
from infra.db.models.users import User as UserDto, UserRole as UserRoleDto


def convert_user_entity_to_dict(user: UserEntity) -> Mapping[str, Any]:
    entity_dict = {
        "username": user.username.as_json(),
        "password": user.password.as_json(),
        "email": user.email.as_json(),
        "date_birth": user.date_birth,
        "first_name": user.first_name.as_json(),
        "last_name": user.last_name.as_json(),
        "bio": user.bio,
        "avatar": user.avatar,
        "verify": user.verify,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }
    if user.role.id is not None:
        entity_dict["role_id"] = user.role.id
    return entity_dict


def convert_user_role_dto_to_entity(user_role: UserRoleDto) -> UserRoleEntity:
    return UserRoleEntity(
        id=user_role.id,
        role=user_role.role,
    )


def convert_user_dto_to_entity(user: UserDto) -> UserEntity:
    return UserEntity(
        id=user.id,
        username=UserName(value=user.username, _need_validate=False),
        password=Password(value=user.password, need_hash=False, _need_validate=False),
        email=Email(user.email, _need_validate=False),
        date_birth=user.date_birth,
        first_name=Name(user.first_name, _need_validate=False),
        last_name=Name(user.last_name, _need_validate=False),
        bio=user.bio,
        avatar=user.avatar,
        verify=user.verify,
        created_at=user.created_at,
        updated_at=user.updated_at,
        role=convert_user_role_dto_to_entity(user.role),
    )


def convert_user_dto_not_load_to_entity(user: UserDto) -> UserEntity:
    return UserEntity(
        id=user.id,
        username=UserName(value=user.username, _need_validate=False),
        password=Password(value=user.password, need_hash=False, _need_validate=False),
        email=Email(user.email, _need_validate=False),
        date_birth=user.date_birth,
        first_name=Name(user.first_name, _need_validate=False),
        last_name=Name(user.last_name, _need_validate=False),
        bio=user.bio,
        avatar=user.avatar,
        verify=user.verify,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
