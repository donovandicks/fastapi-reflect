from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from fastapi_reflect.agents.config import AgentDeps, Model
from fastapi_reflect.agents.tools import _list_songs
from fastapi_reflect.types.songs import get_schema


class GeneratedSQLQuery(BaseModel):
    query: str = Field(description="The generated SQL query")


SQLAgent = Agent(
    model=Model,
    result_type=GeneratedSQLQuery,
    deps_type=AgentDeps,
)


@SQLAgent.system_prompt
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


@SQLAgent.tool
def list_songs(ctx: RunContext[AgentDeps]) -> list[str]:
    """List all current songs in the database.

    Returns:
        list[str]: A list of JSON-stringified song objects from the database
    """
    return _list_songs(ctx)
