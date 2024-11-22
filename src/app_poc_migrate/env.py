import asyncio
import sys

import alembic
import asyncpg
import sqlalchemy as sa
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = alembic.context.config

target_metadata = None


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def db_name() -> str | None:
    args = alembic.context.get_x_argument(as_dictionary=True)
    return args.get("db_name")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    alembic.context.configure(
        url="postgresql+asyncpg://main:abc@localhost:5476/main",
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


def do_run_migrations(connection: sa.engine.Connection) -> None:
    alembic.context.configure(connection, target_metadata=target_metadata)

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    config_values = config.get_section(config.config_ini_section)
    config_values["sqlalchemy.url"] = (
        "postgresql+asyncpg://main:abc@localhost:5476/main"
    )

    connectable = sqlalchemy_asyncio.AsyncEngine(
        sa.engine_from_config(
            config_values,
            prefix="sqlalchemy.",
            poolclass=sa.pool.NullPool,
            future=True,
            connect_args={"server_settings": {"jit": "off"}},
        )
    )

    # pylint: disable-next=too-many-try-statements
    try:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    except (ConnectionError, asyncpg.exceptions.CannotConnectNowError):
        sys.exit(1)

    await connectable.dispose()


if alembic.context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
