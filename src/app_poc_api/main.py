import contextlib
import http
import logging

import fastapi

from app_poc import actions, database
from app_poc.orm import core
from app_poc_api import depends, schema


def start() -> fastapi.FastAPI:
    @contextlib.asynccontextmanager
    async def db_session_maker(_app: fastapi.FastAPI) -> None:
        depends.set_session(database.init("api"))
        yield

    app = fastapi.FastAPI(
        title="app-poc",
        version="DEBUG",
        debug=True,
        lifespan=db_session_maker,
        swagger_ui_parameters={
            "displayRequestDuration": True,
            "filter": True,
            "tryItOutEnabled": True,
            "defaultModelRendering": "model",
        },
    )

    app.include_router(router)

    return app


router = fastapi.APIRouter()


@router.get("/ping")
async def ping(request: fastapi.Request) -> dict:
    logging.debug("Ping received from %s", request.client)
    return {
        "client": request.client,
        "cookies": request.cookies,
        "debug": request.app.debug,
        "healthy": True,
    }


@router.get("/tvshow", response_model=schema.TvshowOut)
async def get_tvshow(tvshow: depends.TvshowById):
    return tvshow


@router.get("/tvshow/find")
async def find_tvshow_by_name(tvshows: depends.TvshowByName):
    return tvshows


@router.put("/tvshow", status_code=http.HTTPStatus.ACCEPTED)
async def update_tvshow(
    tvshow: depends.TvshowById, session: depends.Db, name: str
) -> None:
    await actions.tv.update(session, tvshow, name)


@router.post("/episode", status_code=http.HTTPStatus.ACCEPTED)
async def create_episode(
    session: depends.Db, tvshow: depends.TvshowById, xfile: schema.EpisodeNew
) -> None:
    await actions.tv.create_episode(
        session,
        tvshow,
        xfile.season,
        xfile.episode,
        xfile.episode_overall,
        xfile.name,
        xfile.air_date,
        xfile.channels,
    )


@router.post("/channel-details", response_model=list[schema.ChannelDetail])
async def channel_details(session: depends.Db) -> list[core.ChannelDetail]:
    return await actions.tv.channel_details(session)
