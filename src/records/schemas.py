from schemas import BaseOrmModel
from datetime import datetime


class RecordBase(BaseOrmModel):
    body: str


class RecordCreate(RecordBase):
    pass


class RecordUpdate(RecordBase):
    id: int


class Record(RecordBase):
    id: int
    created_at: datetime
    user_id: int
    likes: int = 0
    dislikes: int = 0