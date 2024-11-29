from fastapi import APIRouter

from fastapi_reflect.services.ai import Deps, agent
from fastapi_reflect.services.songs import SongService
from fastapi_reflect.types.ai import GenerateQueryRequest, GenerateQueryResponse

ai_router = APIRouter(prefix="/v1/ai", tags=["ai"])


@ai_router.post("/query")
async def gen_query(req: GenerateQueryRequest) -> GenerateQueryResponse:
    deps = Deps(songs=SongService())
    result = await agent.run(user_prompt=req.user_prompt, deps=deps)
    return GenerateQueryResponse(generated_request=result.data)
