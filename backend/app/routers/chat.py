from fastapi import APIRouter
from app.services import llm, prompt_builder
from pydantic import BaseModel

router = APIRouter(prefix="/chat")

class PromptRequest(BaseModel):
    character: str
    prompt: str = None

@router.post('/start')
async def start(request: PromptRequest):
    return llm.start_conversation(request.character)

@router.post('/generate')
async def generate(request: PromptRequest):
    reply = llm.get_response(request)
    return reply