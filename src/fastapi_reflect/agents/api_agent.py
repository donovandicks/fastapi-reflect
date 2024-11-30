from dataclasses import dataclass

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from fastapi_reflect.agents.config import Model
from fastapi_reflect.services.docs import DocsService
from fastapi_reflect.services.songs import SongService


@dataclass
class APIDeps:
    songs: SongService


class GeneratedAPIRequest(BaseModel):
    request: str = Field(description="The generated code to send a request")


agent = Agent(
    model=Model,
    result_type=GeneratedAPIRequest,
    deps_type=APIDeps,
)


@agent.system_prompt
def system_prompt() -> str:
    prompt = f"""\
You are given the following OpenAPI Spec:

```
{DocsService.get_spec()}
```

Generate code that sends an API request that correspond to the user's query.
Implement the request in the language or with the tool specified by the user. If
no language or tool is specified, default to `curl`.

Ensure the host, port, endpoint, path and query parameters, and other URL
componenets align with the provided OpenAPI spec.

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
def list_songs(ctx: RunContext[APIDeps]) -> list[str]:
    """List all current songs in the database."""
    return [song.model_dump_json() for song in ctx.deps.songs.list()]
