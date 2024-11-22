import typing

import fastapi

from app_poc import database, query
from app_poc.orm import core

_session_factory: database.SessionFactory | None = None


def set_session(db_: database.SessionFactory) -> None:
    global _session_factory
    _session_factory = db_


async def _db() -> database.SessionFactory:
    if not _session_factory:
        raise Exception
    return _session_factory


Db = typing.Annotated["database.SessionFactory", fastapi.Depends(_db)]


async def _tvshow_by_id(db: Db, tvshow_id: int) -> core.Tvshow:
    async with db() as session, session.begin():
        tvshow = await query.tvshow.get_by_id(session, tvshow_id)
        episodes = await tvshow.awaitable_attrs.episodes
        for episode in episodes:
            await episode.awaitable_attrs.channels

    return tvshow


TvshowById = typing.Annotated[core.Tvshow, fastapi.Depends(_tvshow_by_id)]


async def _tvshow_by_name(db: Db, name: str) -> list[core.Tvshow]:
    async with db() as session, session.begin():
        tvshows = await query.tvshow.list_by_name(session, name)
        for tvshow in tvshows or []:
            episodes = await tvshow.awaitable_attrs.episodes
            for episode in episodes:
                await episode.awaitable_attrs.channels

    return tvshows


TvshowByName = typing.Annotated[core.Tvshow, fastapi.Depends(_tvshow_by_name)]
