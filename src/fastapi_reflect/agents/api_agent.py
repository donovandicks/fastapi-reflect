from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from fastapi_reflect.agents.config import AgentDeps, Model
from fastapi_reflect.agents.tools import _list_songs
from fastapi_reflect.services.docs import DocsService


class GeneratedAPIRequest(BaseModel):
    request: str = Field(description="The generated code to send a request")


APIAgent = Agent(
    model=Model,
    result_type=GeneratedAPIRequest,
    deps_type=AgentDeps,
)


@APIAgent.system_prompt
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


@APIAgent.tool
def list_songs(ctx: RunContext[AgentDeps]) -> list[str]:
    """List all current songs in the database.

    Returns:
        list[str]: A list of JSON-stringified song objects from the database
    """
    return _list_songs(ctx)
