import asyncio

from db import Base, engine

async def init_db():
    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        print("Database created successfully")
    except Exception as e:
        print(f"Error initializing the database: {e}")
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
