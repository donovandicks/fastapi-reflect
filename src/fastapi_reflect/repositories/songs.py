from pydantic import UUID4

from fastapi_reflect.types.songs import Song


class SongRepository:
    _store: dict[UUID4, Song]

    def __init__(self) -> None:
        self._store = {}

    def list(self) -> list[Song]:
        return list(self._store.values())

    def get(self, id: UUID4) -> Song | None:
        return self._store.get(id, None)

    def create(self, song: Song) -> Song:
        self._store[song.id] = song
        return song

    def delete(self, id: UUID4) -> None:
        del self._store[id]
