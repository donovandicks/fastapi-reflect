from typing import Sequence

from pydantic import UUID4

from fastapi_reflect.repositories.songs import InMemRepository, Repository
from fastapi_reflect.types.songs import CreateSongRequest, Song
from fastapi_reflect.utils.singleton import SingletonMeta


class SongService(metaclass=SingletonMeta):
    _repo: Repository

    def __init__(self, repo: Repository | None = None) -> None:
        if not repo:
            repo = InMemRepository()
        self._repo = repo

    def create(self, req: CreateSongRequest) -> Song:
        record = Song.from_request(req)
        return self._repo.create(record)

    def delete(self, id: UUID4) -> None:
        return self._repo.delete(id)

    def list(self) -> Sequence[Song]:
        return self._repo.list()

    def get(self, id: UUID4) -> Song | None:
        return self._repo.get(id)
