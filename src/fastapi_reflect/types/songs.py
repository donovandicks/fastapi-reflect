import uuid

from pydantic import UUID4, BaseModel
from sqlalchemy.schema import CreateTable
from sqlmodel import Field, SQLModel

from fastapi_reflect.datastore import engine


class CreateSongRequest(BaseModel):
    name: str = Field(description="Name of the song")
    runtime: int = Field(description="Length of the song in seconds")
    artist: str = Field(description="Name of the artist that performs the song")
    album: str = Field(description="Name of the album on which the song appears")


class Song(SQLModel, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field()
    runtime: int = Field()
    artist: str = Field()
    album: str = Field()

    @classmethod
    def from_request(cls, req: CreateSongRequest) -> "Song":
        return Song(**req.model_dump())


SQLModel.metadata.create_all(engine)


def get_schema() -> str:
    schema = ""
    for table in SQLModel.metadata.tables.values():
        schema += f"{CreateTable(table, if_not_exists=True).compile(engine)}\n".replace(
            ")\n", ");\n"
        )

    return schema.strip()
