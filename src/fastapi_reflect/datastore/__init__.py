import os
from enum import StrEnum

from sqlmodel import create_engine

from .repository import Repository

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:password@localhost:5433/songs"
)

engine = create_engine(DATABASE_URL)


class RepositoryKind(StrEnum):
    InMemory = "IN_MEMORY"
    Postgres = "POSTGRES"


__all__ = ["engine", "Repository", "RepositoryKind"]
