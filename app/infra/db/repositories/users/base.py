from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.users import User as UserEntity


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
