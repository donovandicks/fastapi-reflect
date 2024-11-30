from dataclasses import dataclass
from typing import Final

from pydantic_ai import Agent, RunContext
from pydantic_ai.models import KnownModelName

from fastapi_reflect.services.docs import DocsService
from fastapi_reflect.services.songs import SongService
from fastapi_reflect.types.ai import APIRequest
from fastapi_reflect.types.songs import get_schema

model: Final[KnownModelName] = "openai:gpt-4o-mini"


@dataclass
class Deps:
    songs: SongService


agent = Agent(
    model=model,
    result_type=APIRequest,
    deps_type=Deps,
)


@agent.system_prompt
def system_prompt() -> str:
    prompt = f"""\
You are given the following OpenAPI Spec:

```
{DocsService.get_spec()}
```

And the following database schema:

```
{get_schema()}
```

Generate curl commands that correspond to the user's query. Ensure the host, port,
endpoint, path and query parameters, and other URL componenets match the provided
OpenAPI spec.

If a user requests commands related to a real data, use tools to retrieve data
from the database.

Example
    Query: How can I list all songs?
    Response: curl http://127.0.0.1:8000/api/v1/songs

Example
    Query: How can I get an individual song?
    Response: curl http://127.0.0.1:8000/api/v1/songs/<Song UUID>
    """

    return prompt


@agent.tool
def list_songs(ctx: RunContext[Deps]) -> list[str]:
    """List all current songs in the database."""
    return [song.model_dump_json() for song in ctx.deps.songs.list()]
