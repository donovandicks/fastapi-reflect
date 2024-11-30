import os

from sqlmodel import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5433/songs"
)

engine = create_engine(DATABASE_URL)

__all__ = ["engine"]
