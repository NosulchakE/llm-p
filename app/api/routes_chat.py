# app/api/routes_chat.py
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.chat import ChatRequest, ChatResponse, MessageResponse
from app.usecases.chat import ChatUseCase
from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Отправка запроса к LLM"""
    try:
        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=request.prompt,
            system=request.system,
            max_history=request.max_history,
            temperature=request.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))


@router.get("/history", response_model=list[MessageResponse])
async def get_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Получение истории диалога"""
    messages = await chat_usecase.get_history(user_id)
    return messages


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Очистка истории диалога"""
    await chat_usecase.clear_history(user_id)
