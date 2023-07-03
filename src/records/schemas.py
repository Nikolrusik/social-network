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
