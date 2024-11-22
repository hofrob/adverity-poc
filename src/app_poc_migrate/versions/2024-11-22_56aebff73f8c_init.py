"""init.

Revision ID: 56aebff73f8c
Revises:
Create Date: 2024-11-22 00:36:21.738247+01:00
"""

import pathlib

from alembic import op
import faker
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "56aebff73f8c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tvshow",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column(
            "uuid",
            postgresql.UUID,
            unique=True,
            nullable=False,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("name", sa.Text),
    )
    op.create_table(
        "episode",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column(
            "uuid",
            postgresql.UUID,
            unique=True,
            nullable=False,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True)),
        sa.Column(
            "tvshow_id",
            sa.BigInteger,
            sa.ForeignKey("tvshow.id"),
            index=True,
            nullable=False,
        ),
        sa.Column("name", sa.Text),
        sa.Column("season", sa.BIGINT),
        sa.Column("number", sa.BIGINT),
        sa.Column("number_overall", sa.BIGINT),
        sa.Column("air_date", sa.TIMESTAMP(timezone=True)),
    )
    op.create_table(
        "channel",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column(
            "uuid",
            postgresql.UUID,
            unique=True,
            nullable=False,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True)),
        sa.Column("name", sa.Text),
    )
    op.create_table(
        "channel_episode",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column(
            "uuid",
            postgresql.UUID,
            unique=True,
            nullable=False,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=True)),
        sa.Column(
            "channel_id",
            sa.BigInteger,
            sa.ForeignKey("channel.id"),
            index=True,
            nullable=False,
        ),
        sa.Column(
            "episode_id",
            sa.BigInteger,
            sa.ForeignKey("episode.id"),
            index=True,
            nullable=False,
        ),
    )

    connection = op.get_bind()
    fake = faker.Faker()
    for _ in range(20):
        connection.execute(
            sa.text("""
                INSERT INTO tvshow (name)
                VALUES (:name)
            """),
            {"name": fake.word()},
        )

    for _ in range(200):
        connection.execute(
            sa.text("""
                INSERT INTO episode (tvshow_id, season, number, number_overall, name, air_date)
                VALUES (:tvshow_id, :season, :number, :number_overall, :name, :air_date)
            """),
            {
                "tvshow_id": fake.random_element(range(1, 20)),
                "season": fake.random_digit(),
                "number": fake.random_digit(),
                "number_overall": fake.random_digit(),
                "name": fake.sentence(nb_words=3),
                "air_date": fake.date_time(),
            },
        )

    for _ in range(40):
        connection.execute(
            sa.text("""
                INSERT INTO channel (name)
                VALUES (:name)
            """),
            {"name": fake.word()},
        )

    for _ in range(100):
        connection.execute(
            sa.text("""
                INSERT INTO channel_episode (channel_id, episode_id)
                VALUES (:channel_id, :episode_id)
            """),
            {
                "channel_id": fake.random_element(range(1, 40)),
                "episode_id": fake.random_element(range(1, 200)),
            },
        )

    with (
        pathlib.Path(__file__).parent.parent / "views" / "public.channel_detail.sql"
    ).open() as sql_file:
        sql = sql_file.read()

    op.execute(sa.text(sql))
