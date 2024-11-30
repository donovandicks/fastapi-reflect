from typing import Sequence

import sqlalchemy
from pydantic import UUID4
from sqlmodel import Session, delete, select

from fastapi_reflect.datastore import Repository, RepositoryKind, engine
from fastapi_reflect.types.songs import Song


def new_song_repository(kind: RepositoryKind) -> Repository[Song]:
    match kind:
        case RepositoryKind.InMemory:
            return InMemRepository()
        case RepositoryKind.Postgres:
            return PostgresRepository()


class InMemRepository(Repository[Song]):
    _store: dict[UUID4, Song]

    def __init__(self) -> None:
        self._store = {}

    def list(self) -> Sequence[Song]:
        return list(self._store.values())

    def get(self, id: UUID4) -> Song | None:
        return self._store.get(id, None)

    def create(self, song: Song) -> Song:
        self._store[song.id] = song
        return song

    def delete(self, id: UUID4) -> None:
        del self._store[id]


class PostgresRepository(Repository[Song]):
    def list(self) -> Sequence[Song]:
        with Session(engine) as s:
            return s.exec(select(Song)).all()

    def get(self, id: UUID4) -> Song | None:
        with Session(engine) as s:
            try:
                return s.get_one(Song, ident=id)
            except sqlalchemy.orm.exc.NoResultFound:
                return None

    def create(self, song: Song) -> Song:
        with Session(engine, expire_on_commit=False) as s:
            s.add(song)
            s.commit()
        return song

    def delete(self, id: UUID4) -> None:
        assert id, "delete clause missing id"
        with Session(engine) as s:
            s.exec(delete(Song).where(Song.id == id))  # type: ignore
            s.commit()
