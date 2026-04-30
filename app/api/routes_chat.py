# app/api/routes_chat.py
from fastapi import APIRouter, Depends, HTTPException, status
import traceback

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
    print("\n" + "="*60)
    print("🎯 [ROUTE] POST /chat ВЫЗВАН!")
    print(f"🎯 [ROUTE] user_id={user_id}")
    print(f"🎯 [ROUTE] prompt={request.prompt}")
    print(f"🎯 [ROUTE] system={request.system}")
    print(f"🎯 [ROUTE] max_history={request.max_history}")
    print(f"🎯 [ROUTE] temperature={request.temperature}")
    print("="*60)
    
    try:
        print("📞 [ROUTE] Вызов usecase.ask()...")
        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=request.prompt,
            system=request.system,
            max_history=request.max_history,
            temperature=request.temperature,
        )
        print(f"✅ [ROUTE] Получен ответ: {answer[:100]}...")
        return ChatResponse(answer=answer)
        
    except ExternalServiceError as e:
        print(f"❌ [ROUTE] ExternalServiceError: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, 
            detail=str(e)
        )
        
    except Exception as e:
        print(f"❌ [ROUTE] Неожиданная ошибка: {type(e).__name__}: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}"
        )


@router.get("/history", response_model=list[MessageResponse])
async def get_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Получение истории диалога"""
    print(f"📜 [ROUTE] GET /history вызван для user_id={user_id}")
    messages = await chat_usecase.get_history(user_id)
    return messages


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    chat_usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Очистка истории диалога"""
    print(f"🗑️ [ROUTE] DELETE /history вызван для user_id={user_id}")
    await chat_usecase.clear_history(user_id)


@router.post("/diagnostic")
async def diagnostic(
    user_id: int = Depends(get_current_user_id),
):
    """Диагностический эндпоинт для проверки OpenRouter"""
    import httpx
    from app.core.config import settings
    
    print(f"🔍 [DIAGNOSTIC] Вызван для user_id={user_id}")
    
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "HTTP-Referer": settings.OPENROUTER_SITE_URL,
        "X-Title": settings.OPENROUTER_APP_NAME,
        "Content-Type": "application/json",
    }
    
    print(f"🔍 [DIAGNOSTIC] Headers being sent: {headers}")  # ← добавить эту строку
    
    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": "Say 'Hello, diagnostic works!'"}],
    }
    
    print(f"🔍 [DIAGNOSTIC] URL: {settings.OPENROUTER_BASE_URL}/chat/completions")
    print(f"🔍 [DIAGNOSTIC] Model: {settings.OPENROUTER_MODEL}")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{settings.OPENROUTER_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                follow_redirects=True,
            )
            
            print(f"🔍 [DIAGNOSTIC] Response status: {response.status_code}")
            
            return {
                "status": response.status_code,
                "headers": dict(response.headers),
                "text": response.text[:500],
            }
            
        except Exception as e:
            print(f"❌ [DIAGNOSTIC] Ошибка: {e}")
            return {
                "status": 500,
                "error": str(e),
            }
