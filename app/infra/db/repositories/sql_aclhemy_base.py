from dataclasses import dataclass
from typing import Type

from sqlalchemy import select, insert
from sqlalchemy.orm import DeclarativeBase

from infra.db.db_config import Database


@dataclass(eq=False)
class SqlAlchemyRepository[Model: DeclarativeBase]:
    model: Type[Model]
    database: Database

    async def find_one_or_none(self, **filters) -> Model:
        async with self.database.get_read_only_session() as session:
            query = select(self.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def add_one(self, **data) -> Model:
        async with self.database.get_session() as session:
            query = insert(self.model).values(**data).returning(self.model)
            result = await session.execute(query)
            new_object = result.scalar()
            await session.commit()
            return new_object
