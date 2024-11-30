from pydantic_ai import RunContext

from fastapi_reflect.agents.config import AgentDeps


def _list_songs(ctx: RunContext[AgentDeps]) -> list[str]:
    return [song.model_dump_json() for song in ctx.deps.songs.list()]
