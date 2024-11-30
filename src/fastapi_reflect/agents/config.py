from dataclasses import dataclass
from typing import Final

from pydantic_ai.models import KnownModelName

from fastapi_reflect.services.songs import SongService

Model: Final[KnownModelName] = "openai:gpt-4o-mini"


@dataclass
class AgentDeps:
    songs: SongService
