"""
db_connection.py

Database connection management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import Config


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{Config.DB_USER}:"
    f"{Config.DB_PASSWORD}@"
    f"{Config.DB_HOST}:"
    f"{Config.DB_PORT}/"
    f"{Config.DB_NAME}"
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def get_session():
    """
    Returns database session.
    """

    return SessionLocal()