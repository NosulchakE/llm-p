# app/usecases/chat.py
import traceback

from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(self, message_repo: ChatMessageRepository, llm_client: OpenRouterClient):
        self._message_repo = message_repo
        self._llm_client = llm_client
    
    async def ask(self, user_id: int, prompt: str, system: str | None, max_history: int, temperature: float) -> str:
        print("\n [USECASE] ask() начал")
        print(f"[USECASE] user_id={user_id}")
        print(f"[USECASE] prompt={prompt}")
        print(f"[USECASE] system={system}")
        print(f"[USECASE] max_history={max_history}")
        print(f"[USECASE] temperature={temperature}")
        
        messages = []
        
        if system:
            messages.append({"role": "system", "content": system})
            print("[USECASE] Добавлен system message")
        
        try:
            print("[USECASE] Запрос истории из БД...")
            history = await self._message_repo.get_last_messages(user_id, max_history)
            print(f"[USECASE] Получено {len(history)} сообщений из истории")
            
            for msg in history:
                messages.append({"role": msg.role, "content": msg.content})
            
            messages.append({"role": "user", "content": prompt})
            print(f"[USECASE] Всего messages: {len(messages)}")
            
            print("[USECASE] Сохранение пользовательского сообщения...")
            await self._message_repo.add_message(user_id, "user", prompt)
            print("[USECASE] Сообщение пользователя сохранено")
            
            print("[USECASE] Вызов LLM клиента...")
            answer = await self._llm_client.chat_completion(messages)
            print(f"[USECASE] Получен ответ от LLM: {answer[:100]}...")
            
            print("[USECASE] Сохранение ответа ассистента...")
            await self._message_repo.add_message(user_id, "assistant", answer)
            print("[USECASE] Ответ ассистента сохранён")
            
            print("[USECASE] ask() успешно завершён")
            return answer
            
        except Exception as e:
            print(f"[USECASE] Ошибка: {type(e).__name__}: {str(e)}")
            traceback.print_exc()
            raise
    
    async def get_history(self, user_id: int, limit: int = 50) -> list:
        print(f"[USECASE] get_history() вызван для user_id={user_id}")
        messages = await self._message_repo.get_last_messages(user_id, limit)
        print(f"[USECASE] Возвращено {len(messages)} сообщений")
        return messages
    
    async def clear_history(self, user_id: int) -> None:
        print(f"[USECASE] clear_history() вызван для user_id={user_id}")
        await self._message_repo.delete_user_history(user_id)
        print("[USECASE] История очищена")
