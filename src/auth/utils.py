import httpx

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import get_async_session
from config import EMAIL_CHECK_API_KEY


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


def check_email_existence(email: str) -> bool:
    '''
    Checks the existence of the specified email address using the Hunter.io API.

    Arguments:
    email (str): The email address to be checked.

    Returns:
    bool: True if the email exists and is deliverable, False otherwise.
    '''
    base_url = 'https://api.hunter.io/v2'
    api_key = EMAIL_CHECK_API_KEY

    with httpx.Client() as client:
        response = client.get(
            f'{base_url}/email-verifier',
            params={'email': email, 'api_key': api_key}
        )

        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('result', 'unknown') == 'deliverable'

        return False