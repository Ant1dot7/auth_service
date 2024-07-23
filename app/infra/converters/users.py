from dataclasses import asdict
from typing import Any, Mapping

from domain.entities.users import User as UserEntity
from domain.entities.users import UserRole as UserRoleEntity
from domain.values.users import UserName, Password, Email, Name
from infra.db.models.users import User as UserDto
from infra.db.models.users import UserRole as UserRoleDto


def convert_user_entity_to_dict(user: UserEntity) -> Mapping[str, Any]:
    return {
        'username': user.username.as_json(),
        'password': user.password.as_json(),
        'email': user.email.as_json(),
        'date_birth': user.date_birth,
        'first_name': user.first_name.as_json(),
        'last_name': user.last_name.as_json(),
        'bio': user.bio,
        'avatar': user.avatar,
        'verify': user.verify,
        'created_at': user.created_at,
        'updated_at': user.updated_at,
        "role_id": user.role.id,
    }


def convert_user_role_dto_to_entity(user_role: UserRoleDto) -> UserRoleEntity:
    return UserRoleEntity(
        id=user_role.id,
        role=user_role.role
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
        role=convert_user_role_dto_to_entity(user.role)
    )
