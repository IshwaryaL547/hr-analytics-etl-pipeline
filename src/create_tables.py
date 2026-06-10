"""
create_tables.py

Creates all Silver, Gold and Audit tables.
"""

from src.db_connection import engine
from src.logger import logger
from models.hr_models import Base


def create_all_tables():
    """
    Create all tables.
    """

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "All tables created successfully."
    )
    logger.info(
        "Creating database tables..."
    )

if __name__ == "__main__":

    create_all_tables()