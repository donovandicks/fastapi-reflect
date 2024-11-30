from typing import Sequence

from pydantic import UUID4

from fastapi_reflect.datastore import Repository, RepositoryKind
from fastapi_reflect.repositories.songs import new_song_repository
from fastapi_reflect.types.songs import CreateSongRequest, Song
from fastapi_reflect.utils.singleton import SingletonMeta


class SongService(metaclass=SingletonMeta):
    _repo: Repository

    def __init__(self, repo: Repository | None = None) -> None:
        if not repo:
            repo = new_song_repository(RepositoryKind.InMemory)
        self._repo = repo

    def create(self, req: CreateSongRequest) -> Song:
        song = Song.from_request(req)
        return self._repo.create(song)

    def delete(self, id: UUID4) -> None:
        return self._repo.delete(id)

    def list(self) -> Sequence[Song]:
        return self._repo.list()

    def get(self, id: UUID4) -> Song | None:
        return self._repo.get(id)
