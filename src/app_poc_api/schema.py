import datetime
import uuid

import pydantic


class Channel(pydantic.BaseModel):
    name: str


class EpisodeOut(pydantic.BaseModel):
    id: int
    uuid: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    season: int
    number: int
    number_overall: int
    name: str
    air_date: datetime.datetime | None
    channels: list[Channel]


class TvshowOut(pydantic.BaseModel):
    name: str
    episodes: list[EpisodeOut]


class TvshowList(pydantic.BaseModel):
    id: int
    uuid: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    name: str


class EpisodeNew(pydantic.BaseModel):
    season: int
    episode: int
    episode_overall: int
    name: str
    air_date: datetime.datetime | None
    channels: list[str] = pydantic.Field(default_factory=list)


class ChannelDetail(pydantic.BaseModel):
    id: int
    uuid: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    name: str
    tvshow_names: list[str]
