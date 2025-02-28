import datetime

from sqlalchemy import Column, DateTime, Integer

from app.db.database import Base


class BaseModel(Base):
    """Base class for all SQLAlchemy models"""

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    created_at = Column(DateTime, default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(
        DateTime,
        default=datetime.datetime.now(datetime.UTC),
        onupdate=datetime.datetime.now(datetime.UTC),
    )
