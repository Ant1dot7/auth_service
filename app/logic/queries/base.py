from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(eq=False)
class BaseQuery(ABC):
    filters: dict | None


@dataclass(eq=False)
class QueryHandler[Query, QueryResult: Any](ABC):
    @abstractmethod
    async def handle(self, query: Query) -> QueryResult:
        ...
