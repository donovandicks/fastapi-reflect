from abc import ABC
from typing import Sequence

import sqlalchemy
from pydantic import UUID4
from sqlmodel import Session, select

from fastapi_reflect.datastore import engine
from fastapi_reflect.types.songs import Song


class Repository(ABC):
    def list(self) -> Sequence[Song]: ...
    def get(self, id: UUID4) -> Song | None: ...
    def create(self, song: Song) -> Song: ...
    def delete(self, id: UUID4) -> None: ...


class InMemRepository(Repository):
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


class PostgresRepository(Repository):
    def __init__(self) -> None:
        pass

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
        with Session(engine) as s:
            s.add(song)
            s.commit()
        return song

    def delete(self, id: UUID4) -> None:
        with Session(engine) as s:
            maybe_song = self.get(id=id)
            if maybe_song:
                s.delete(maybe_song)
                s.commit()
