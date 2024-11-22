from collections import abc
import typing

from sqlalchemy import orm, select
from sqlalchemy.ext import asyncio


def create_one_by(model, attribute):
    async def get_by(session: asyncio.AsyncSession, value: typing.Any) -> model:
        query = select(model).where(attribute == value)
        result = await session.execute(query)
        return result.scalar_one()

    return get_by


def create_list_by(model, conditions=None, joins=None):
    async def list_by(session: asyncio.AsyncSession) -> abc.Sequence[model]:
        query = select(model)
        if conditions:
            query = query.where(*conditions)
        if joins:
            query = query.options(orm.selectinload(*joins))
        result = await session.execute(query)
        return result.scalars().all()

    return list_by
