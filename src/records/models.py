from datetime import datetime

from sqlalchemy import TIMESTAMP, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.models import User

from database import Base


class Record(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    body: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(
        'User', back_populates='records'
    )

    def __repr__(self):
        return f'Record(id={self.id}, body={self.name}, user_id={self.user_id})'
