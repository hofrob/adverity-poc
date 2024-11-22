
from typing import TYPE_CHECKING

from app_poc.orm import core
from app_poc.query import base

if TYPE_CHECKING:
    from sqlalchemy.ext import asyncio

MODEL = core.Tvshow


get_by_id = base.create_one_by(MODEL, MODEL.id)
list_all = base.create_list_by(MODEL, joins=[MODEL.episodes])


async def list_by_name(session: asyncio.AsyncSession, name: str) -> list[MODEL]:
    return await base.create_list_by(MODEL, [MODEL.name.ilike(f"%{name}%")])(session)
