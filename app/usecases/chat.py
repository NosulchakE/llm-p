# app/usecases/chat.py
from typing import List, Dict

from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(self, message_repo: ChatMessageRepository, llm_client: OpenRouterClient):
        self._message_repo = message_repo
        self._llm_client = llm_client
    
    async def ask(self, user_id: int, prompt: str, system: str | None, max_history: int, temperature: float) -> str:
        """Обработка запроса к LLM с сохранением истории"""
        
        # Формируем список сообщений
        messages: List[Dict[str, str]] = []
        
        # Добавляем system инструкцию
        if system:
            messages.append({"role": "system", "content": system})
        
        # Добавляем историю
        history = await self._message_repo.get_last_messages(user_id, max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Добавляем текущий запрос
        messages.append({"role": "user", "content": prompt})
        
        # Сохраняем запрос пользователя
        await self._message_repo.add_message(user_id, "user", prompt)
        
        # Получаем ответ от LLM (temperature пока не используется в простой реализации)
        answer = await self._llm_client.chat_completion(messages)
        
        # Сохраняем ответ модели
        await self._message_repo.add_message(user_id, "assistant", answer)
        
        return answer
    
    async def get_history(self, user_id: int, limit: int = 50) -> list:
        """Получение истории диалога"""
        return await self._message_repo.get_last_messages(user_id, limit)
    
    async def clear_history(self, user_id: int) -> None:
        """Очистка истории диалога"""
        await self._message_repo.delete_user_history(user_id)
