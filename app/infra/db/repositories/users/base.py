from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.users import User as UserEntity
from domain.entities.users import UserRole as UserRoleEntity


@dataclass(eq=False)
class BaseUserRoleRepository(ABC):
    @abstractmethod
    async def get_role(self, **filters) -> UserRoleEntity:
        ...


@dataclass(eq=False)
class BaseUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    async def get_user(self, **filters) -> UserEntity:
        ...

    @abstractmethod
    async def exists_user(self, **filters) -> bool:
        ...

    @abstractmethod
    async def update_user(self, user: UserEntity):
        ...
