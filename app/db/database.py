from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Create SQLAlchemy engine with the database URL from settings
engine = create_engine(
    settings.db_url,
    # For PostgreSQL in production:
    # connect_args={"connect_timeout": 10},
    # pool_pre_ping=True,
    # pool_recycle=300,
)

# Create SessionLocal class with sessionmaker
# This will be used to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for our SQLAlchemy models
# All database models will inherit from this class
Base = declarative_base()


# Dependency function for FastAPI to get a DB session
def get_db() -> Generator:
    """
    Dependency function that yields a SQLAlchemy session and ensures it gets closed
    after the request is complete, even if an exception occurs.

    Yields:
        Generator: SQLAlchemy session that can be used for database operations
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
