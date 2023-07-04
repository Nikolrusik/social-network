from datetime import datetime
from enum import Enum
from sqlalchemy import TIMESTAMP, Integer, String, ForeignKey, Enum as EnumType
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, metadata


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    body: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id', ondelete='CASCADE'))

    user = relationship(
        'User', backref='records'
    )

    def __repr__(self):
        return f'Record(id={self.id}, body={self.name}, user_id={self.user_id})'
    

class LikeOrDislike(Enum):
        DISLIKE = '0'
        LIKE = '1'


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    record_id: Mapped[int] = mapped_column(Integer, ForeignKey('records.id', ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id', ondelete='CASCADE'))
    like: Mapped[str] = mapped_column(
        EnumType(LikeOrDislike, name='like')
    )

    user = relationship(
        'User', backref='likes'
    )

    def __repr__(self):
        return f'Like(id={self.id}, record_id={self.record_id}, user_id={self.user_id}'