import uuid

from pydantic import UUID4, BaseModel, Field


class CreateSongRequest(BaseModel):
    name: str = Field(description="Name of the song")
    runtime: int = Field(description="Length of the song in seconds")
    artist: str = Field(description="Name of the artist that performs the song")
    album: str = Field(description="Name of the album on which the song appears")


class Song(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    name: str = Field(description="Name of the song")
    runtime: int = Field(description="Length of the song in seconds")
    artist: str = Field(description="Name of the artist that performs the song")
    album: str = Field(description="Name of the album on which the song appears")

    @classmethod
    def from_request(cls, req: CreateSongRequest) -> "Song":
        return Song(**req.model_dump())
