from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import get_config

engine = create_async_engine(get_config(), pool_pre_ping=True)
LocalSession = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass



async def get_db() -> AsyncIterator[AsyncSession]:

    async with LocalSession() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


Session = Annotated[AsyncSession, Depends(get_db)]
