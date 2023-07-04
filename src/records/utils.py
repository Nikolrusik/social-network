from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from records import models as md


async def count_likes(record_id: int, session: AsyncSession) -> int:
    '''
    Returned count likes for record
    '''
    query = select(func.count()).where(md.Like.record_id == record_id, md.Like.like == md.LikeOrDislike.LIKE)
    result = await session.execute(query)
    return result.scalar()

async def count_dislikes(record_id: int, session: AsyncSession) -> int:
    '''
    Returned count dislikes for record
    '''
    query = select(func.count()).where(md.Like.record_id == record_id, md.Like.like == md.LikeOrDislike.DISLIKE)
    result = await session.execute(query)
    return result.scalar()

async def is_liked(record_id: int, user_id: int, session: AsyncSession) -> bool:
    '''
    Returned status like for record
    '''
    query = select(md.Like).where(md.Like.record_id == record_id, md.Like.user_id == user_id)
    result = await session.execute(query)
    like = result.scalar_one_or_none()
    return like is not None
