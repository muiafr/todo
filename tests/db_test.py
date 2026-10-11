import pytest

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


@pytest.mark.asyncio
async def test_database_connection():
    from db.db import engine
    from db.config import get_config

    if engine is None:
        engine = create_async_engine(
            "sqlite+aiosqlite:///./test.db",
            echo=True
        )

    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))

            assert result.scalar() == 1

    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")