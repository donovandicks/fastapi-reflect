from fastapi_reflect.agents.api_agent import APIDeps, GeneratedAPIRequest
from fastapi_reflect.agents.api_agent import agent as APIAgent
from fastapi_reflect.agents.sql_agent import GeneratedSQLQuery, SQLDeps
from fastapi_reflect.agents.sql_agent import agent as SQLAgent
from fastapi_reflect.services.songs import SongService


class AIService:
    @classmethod
    async def gen_api_request(cls, user_prompt: str) -> GeneratedAPIRequest:
        deps = APIDeps(songs=SongService())
        response = await APIAgent.run(user_prompt=user_prompt, deps=deps)
        return response.data

    @classmethod
    async def gen_sql_request(cls, user_prompt: str) -> GeneratedSQLQuery:
        deps = SQLDeps(songs=SongService())
        response = await SQLAgent.run(user_prompt=user_prompt, deps=deps)
        return response.data
