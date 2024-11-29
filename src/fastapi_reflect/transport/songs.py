from http import HTTPStatus

import logfire
from fastapi import APIRouter, HTTPException, Response
from pydantic import UUID4

from fastapi_reflect.repositories.songs import SongRepository
from fastapi_reflect.services.songs import SongService
from fastapi_reflect.types.songs import CreateSongRequest, Song

songs_router = APIRouter(prefix="/v1/songs", tags=["songs"])

repo = SongRepository()
svc = SongService(repo)


@songs_router.get("")
@songs_router.get("/")
def list_songs() -> list[Song]:
    return svc.list()


@songs_router.get("/{id}")
def get_song(id: UUID4) -> Song:
    song = svc.get(id)
    if not song:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=f"No song found for ID {id!r}"
        )
    return song


@songs_router.post("")
@songs_router.post("/")
def create_song(req: CreateSongRequest) -> Song:
    logfire.info(f"received create request: {req=}")
    return svc.create(req)


@songs_router.delete("/{id}")
def delete_song(id: UUID4):
    svc.delete(id)
    return Response(status_code=HTTPStatus.NO_CONTENT)