import sqlalchemy as sa
from sqlalchemy.ext import asyncio

type SessionFactory = asyncio.async_sessionmaker[asyncio.AsyncSession]


HALF_HOUR_IN_SECONDS = 1800


def init(application_name: str) -> SessionFactory:
    url = sa.URL.create("postgresql+asyncpg", "main", "abc", "localhost", 5476, "main")
    engine = asyncio.create_async_engine(
        url,
        pool_recycle=HALF_HOUR_IN_SECONDS,
        pool_reset_on_return="rollback",
        connect_args={
            "server_settings": {
                "application_name": application_name,
                "timezone": "Europe/Vienna",
            }
        },
    )
    return asyncio.async_sessionmaker(
        engine, expire_on_commit=False, autoflush=False, autobegin=False
    )
