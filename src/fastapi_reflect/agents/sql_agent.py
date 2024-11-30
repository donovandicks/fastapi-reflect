from dataclasses import dataclass

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from fastapi_reflect.agents.config import Model
from fastapi_reflect.services.songs import SongService
from fastapi_reflect.types.songs import get_schema


@dataclass
class SQLDeps:
    songs: SongService


class GeneratedSQLQuery(BaseModel):
    query: str = Field(description="The generated SQL query")


agent = Agent(
    model=Model,
    result_type=GeneratedSQLQuery,
    deps_type=SQLDeps,
)


@agent.system_prompt
def system_prompt() -> str:
    prompt = f"""\
Given the following PostgreSQL table schema, your job is to write a SQL query
that suits the user's request.

```
{get_schema()}
```

Example
    Request: show me all fields from all songs
    Response: SELECT * FROM song

Example
    Request: show the id of a song named 'ABC'
    Response: SELECT song.id FROM song WHERE song.name = 'ABC'
    """

    return prompt


@agent.tool
def list_songs(ctx: RunContext[SQLDeps]) -> list[str]:
    """List all current songs in the database."""
    return [song.model_dump_json() for song in ctx.deps.songs.list()]
