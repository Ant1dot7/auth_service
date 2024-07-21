from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@dataclass(eq=False)
class UserUnitOfWork:
    session_maker: async_sessionmaker

    async def __aenter__(self):
        self._session: AsyncSession = self.session_maker()
        # self.user_repository = UserRepository(model=User, session=self._session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self._session.rollback()
        else:
            await self._session.commit()
        await self._session.close()
