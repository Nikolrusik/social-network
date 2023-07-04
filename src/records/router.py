from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from auth.models import User
from auth.base_config import current_user
from database import get_async_session

from schemas import Response
from records import models as md
from records import schemas as sc
from records import utils as ut


router = APIRouter(
    prefix='/record',
    tags=['Records'],
)


@router.get('/list', response_model=Response[List[sc.Record]])
async def get_record_list(
        limit: int = 25,
        offset: int = 0,
        session: AsyncSession = Depends(get_async_session)):
    try:
        '''
        Get a list records
        '''
        query = select(md.Record).limit(limit).offset(offset)
        result = await session.execute(query)
        records = result.scalars().all()

        for record in records:
            record.likes = await ut.count_likes(record.id, session)
            record.dislikes = await ut.count_dislikes(record.id, session)

        return {
            'status': 'success',
            'data': records
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': str(e)
        })


@router.post('/create', response_model=Response[sc.Record])
async def create_record(
    new_record: sc.RecordCreate,
    user:  User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Create new record
    '''
    try:
        record = md.Record(**new_record.dict(), user_id=user.id)
        session.add(record)
        await session.commit()
        return {
            'status': 'success',
            'data': record
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': str(e)
        })


@router.patch('/update/{record_id}', response_model=Response[sc.Record])
async def update_record(
    record_id: int,
    updated_record: sc.RecordUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Update record by id
    '''
    try:
        stmt = select(md.Record).filter(md.Record.id == record_id,
                                        md.Record.user_id == user.id)
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(status_code=404, detail={
                'status': 'error',
                'data': 'Record Not Found'
            })

        update_data = updated_record.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(record, field, value)

        await session.commit()
        await session.refresh(record)
        
        return {
            'status': 'success',
            'data': record
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500, detail={
                'status': 'error',
                'data': 'Failed to update record'
            })


@router.delete('/delete/{id}')
async def delete_stock(
        id: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)):
    '''
    Delete record by id
    '''
    try:
        stmt = delete(md.Record).filter(md.Record.id ==
                                        id, md.Record.user_id == user.id)
        await session.execute(stmt)
        await session.commit()

        return {
            'status': 'success',
            'data': f'Deleted record.id = {id}',
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': str(e)
        })

@router.post('/{record_id}/like')
async def like_record(like_or_dislike: md.LikeOrDislike, record_id: str, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    '''
    Like or dislike record
    '''
    stmt_record = select(md.Record).filter(md.Record.id == record_id)
    result_record = await session.execute(stmt_record)
    record = result_record.scalar_one_or_none() 

    if not record:
        raise HTTPException(status_code=404, detail={
        'status': 'error',
        'data': 'Record Not Found'
    })

    if record.user_id == user.id:
        raise HTTPException(status_code=403, detail={
        'status': 'error',
        'data': 'You cannot rate your own records.'
    })

    is_liked = await ut.is_liked(record.id, user.id, session)

    if is_liked: 
        raise HTTPException(status_code=403, detail={
        'status': 'error',
        'data': 'You have already rated this record.'
    })

    session.add(md.Like(user_id=user.id, record_id=record.id, like=like_or_dislike))
    await session.commit()
    
    return {'message': 'Record liked!'}
