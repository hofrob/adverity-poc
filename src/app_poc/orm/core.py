from collections import abc
import datetime

import sqlalchemy as sa
from sqlalchemy import ForeignKey, orm
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext import asyncio
from sqlalchemy.ext.asyncio import AsyncAttrs


def _column(foreign_table: str) -> sa.Column:
    return sa.Column(f"{foreign_table}_id", sa.ForeignKey(f"{foreign_table}.id"))


def link(left: str, right: str) -> abc.Callable[[], sa.Table]:
    table_name = f"{left}_{right}"

    def _table() -> sa.Table:
        try:
            return next(
                sa_table
                for sa_table in Base.metadata.sorted_tables
                if sa_table.name == table_name
            )
        except StopIteration:
            return sa.Table(table_name, Base.metadata, _column(left), _column(right))

    return _table


class Base(AsyncAttrs, orm.DeclarativeBase): ...


class Model(Base):
    __abstract__ = True
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[sa.Uuid] = orm.mapped_column(
        postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()")
    )
    updated_at: orm.Mapped[datetime.datetime | None] = orm.mapped_column(
        sa.DateTime(timezone=True)
    )
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True)
    )

    def __init__(self, session: asyncio.AsyncSession) -> None:
        super().__init__()
        session.add(self)


class Tvshow(Model):
    __tablename__ = "tvshow"

    name: orm.Mapped[str]

    episodes: orm.Mapped[list[Episode]] = orm.relationship("Episode")


class Episode(Model):
    __tablename__ = "episode"

    tvshow_id: orm.Mapped[int] = orm.mapped_column(ForeignKey(Tvshow.id))
    season: orm.Mapped[int | None]
    number: orm.Mapped[int | None]
    number_overall: orm.Mapped[int | None]
    name: orm.Mapped[str | None]
    air_date: orm.Mapped[datetime.datetime | None] = orm.mapped_column(
        sa.DateTime(timezone=True)
    )

    tvshow: orm.Mapped[Tvshow] = orm.relationship(Tvshow, back_populates="episodes")
    channels: orm.Mapped[list[Channel]] = orm.relationship(
        secondary=link("channel", "episode")
    )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}/{self.name}>"


class Channel(Model):
    __tablename__ = "channel"

    name: orm.Mapped[str | None]

    episodes: orm.Mapped[list[Episode]] = orm.relationship(
        secondary=link("channel", "episode"), back_populates="channels"
    )


class ChannelDetail(Model):
    __tablename__ = "channel_detail"

    name: orm.Mapped[str]
    tvshow_names: orm.Mapped[list[str]] = orm.mapped_column(postgresql.JSONB)
