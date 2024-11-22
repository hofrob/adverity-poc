import typing

from app_poc import query
from app_poc.orm import core

if typing.TYPE_CHECKING:
    import datetime

    from app_poc import database


async def get(session: database.SessionFactory, tvshow_id: int) -> core.Tvshow:
    async with session() as session, session.begin():
        tvshow = await query.tvshow.get_by_id(session, tvshow_id)
        await tvshow.awaitable_attrs.channels
        return tvshow


async def update(session: database.SessionFactory, tvshow: core.Tvshow, name) -> None:
    async with session() as session, session.begin():
        session.add(tvshow)
        tvshow.name = name


async def create_episode(
    session: database.SessionFactory,
    tvshow: core.Tvshow,
    season: int,
    number: int,
    number_overall: int,
    name: str,
    air_date: datetime.datetime | None,
    channels: list[str],
) -> None:
    async with session() as session, session.begin():
        episode = core.Episode(session)
        episode.tvshow = tvshow
        episode.season = season
        episode.episode = number
        episode.episode_overall = number_overall
        episode.name = name
        episode.air_date = air_date

        for channel in channels:
            channel_orm = core.Channel(session)
            channel_orm.name = channel
            episode.channels.append(channel_orm)


async def channel_details(
    session: database.SessionFactory,
) -> list[core.ChannelDetail]:
    async with session() as session, session.begin():
        return await query.channel_detail.list_all(session)
