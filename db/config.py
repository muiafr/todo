import os
from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


def get_config():
    database_url = os.getenv("DB_URL")
    if database_url:
        return database_url

    try:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "postgres"),
            port=int(os.getenv("DB_PORT", "5432")),
        )
    except (TypeError, ValueError) as e:
        raise RuntimeError(f"Invalid database configuration: {e}") from e