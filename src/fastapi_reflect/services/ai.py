from fastapi_reflect.agents.api_agent import APIAgent, GeneratedAPIRequest
from fastapi_reflect.agents.config import AgentDeps
from fastapi_reflect.agents.sql_agent import GeneratedSQLQuery, SQLAgent
from fastapi_reflect.services.songs import SongService


class AIService:
    @classmethod
    async def gen_api_request(cls, user_prompt: str) -> GeneratedAPIRequest:
        deps = AgentDeps(songs=SongService())
        response = await APIAgent.run(user_prompt=user_prompt, deps=deps)
        return response.data

    @classmethod
    async def gen_sql_request(cls, user_prompt: str) -> GeneratedSQLQuery:
        deps = AgentDeps(songs=SongService())
        response = await SQLAgent.run(user_prompt=user_prompt, deps=deps)
        return response.data
