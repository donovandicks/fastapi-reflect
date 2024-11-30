from fastapi import APIRouter

from fastapi_reflect.services.ai import AIService
from fastapi_reflect.types.ai import GenAIRequest, GenAIResponse

ai_router = APIRouter(prefix="/v1/ai", tags=["ai"])


@ai_router.post("/gen-api")
async def gen_api_req(req: GenAIRequest) -> GenAIResponse:
    result = await AIService.gen_api_request(user_prompt=req.user_prompt)
    return GenAIResponse(response=result.request)


@ai_router.post("/gen-sql")
async def gen_sql_qry(req: GenAIRequest) -> GenAIResponse:
    result = await AIService.gen_sql_request(user_prompt=req.user_prompt)
    return GenAIResponse(response=result.query)
