from database import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from datetime import datetime


class TimestampMixin(Base):

    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
