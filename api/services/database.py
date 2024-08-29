from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    AsyncEngine,
    async_scoped_session,
    async_sessionmaker,
)
from contextlib import asynccontextmanager
from asyncio import current_task

from api.services import config

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PostgreSQLController:
    def __init__(self, echo: bool = False) -> None:
        self.engine: AsyncEngine = create_async_engine(
            config.get_connection_string(), echo=echo
        )
        self._session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine, expire_on_commit=False
        )
        self._factory = async_scoped_session(
            self._session_maker, scopefunc=current_task
        )

    async def init_db(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_db(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def __call__(self) -> AsyncSession:  # type: ignore
        try:
            async with self._factory() as s:
                yield s
        finally:
            await self._factory.remove()
