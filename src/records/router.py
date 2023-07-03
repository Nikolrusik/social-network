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
        query = select(md.Record).limit(limit).offset(offset)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.mappings().all()
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
    try:
        with session.begin():
            record = md.Record(**new_record.dict(), user_id=user.id)
            session.add(record)
            await session.commit()
        return {
            'status': 'success',
            'data': record
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': str(e)
        })


@router.put('/update/{record_id}', response_model=Response[sc.Record])
async def update_record(
    record_id: int,
    updated_record: sc.RecordUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    stmt = select(md.Record).filter(md.Record.id == record_id,
                                    md.Record.user_id == user.id)
    record = await session.execute(stmt)

    if not record:
        raise HTTPException(status_code=404, detail={
            'status': 'error',
            'data': 'Record Not Found'
        })
    for field, value in updated_record.dict().items():
        setattr(record, field, value)

    try:
        session.commit()
        session.refresh(record)
        return record
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
    Delete stock by id
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
