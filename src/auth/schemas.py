from fastapi_users import schemas
from auth.utils import check_email_existence
from pydantic import validator, EmailStr, Field



class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    @validator('email')
    def validate_email(cls, email):
        check = check_email_existence(email)
        if not check:
            raise ValueError('Invalid email address')
        return email

class UserUpdate(schemas.BaseUserUpdate):
    pass