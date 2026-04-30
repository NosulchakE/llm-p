# app/services/openrouter_client.py
import httpx
from typing import List, Dict
import traceback

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        print(f"🔧 [INIT] Client created")
        print(f"🔧 [INIT] Base URL: {self.base_url}")
        print(f"🔧 [INIT] Model: {self.model}")
        print(f"🔧 [INIT] API Key (первые 20 символов): {self.api_key[:20] if self.api_key else 'None'}")
    
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        print(f"\n🚀 [CHAT] Начало запроса")
        print(f"🚀 [CHAT] Получено messages: {messages}")
        
        # Проверка API ключа
        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            error_msg = "OpenRouter API key is not configured"
            print(f"❌ [CHAT] {error_msg}")
            raise ExternalServiceError(error_msg)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_APP_NAME,
            "Content-Type": "application/json",
        }
        
        print(f"🔑 [CHAT] Headers: { {k: v[:20] if k == 'Authorization' else v for k, v in headers.items()} }")
        
        payload = {
            "model": self.model,
            "messages": messages,
        }
        
        print(f"📦 [CHAT] Payload: {payload}")
        
        url = f"{self.base_url}/chat/completions"
        print(f"🌐 [CHAT] URL: {url}")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                print(f"⏳ [CHAT] Отправка POST запроса...")
                response = await client.post(
                    url,
                    headers=headers,
                    json=payload,
                    follow_redirects=True,
                )
                
                print(f"✅ [CHAT] Получен ответ. Status: {response.status_code}")
                print(f"📋 [CHAT] Response headers: {dict(response.headers)}")
                print(f"📄 [CHAT] Response text (первые 500 символов): {response.text[:500]}")
                
                if response.status_code == 401:
                    error_msg = f"OpenRouter: Invalid API key - {response.text}"
                    print(f"❌ [CHAT] {error_msg}")
                    raise ExternalServiceError(error_msg)
                elif response.status_code == 429:
                    error_msg = "OpenRouter: Rate limit exceeded"
                    print(f"❌ [CHAT] {error_msg}")
                    raise ExternalServiceError(error_msg)
                elif response.status_code != 200:
                    error_msg = f"OpenRouter error: {response.status_code} - {response.text}"
                    print(f"❌ [CHAT] {error_msg}")
                    raise ExternalServiceError(error_msg)
                
                data = response.json()
                answer = data["choices"][0]["message"]["content"]
                print(f"🎉 [CHAT] Успех! Ответ: {answer[:100]}...")
                return answer
                
            except httpx.TimeoutException:
                error_msg = "OpenRouter timeout after 60 seconds"
                print(f"❌ [CHAT] {error_msg}")
                print(traceback.format_exc())
                raise ExternalServiceError(error_msg)
            except httpx.ConnectError as e:
                error_msg = f"Cannot connect to OpenRouter: {str(e)}"
                print(f"❌ [CHAT] {error_msg}")
                print(traceback.format_exc())
                raise ExternalServiceError(error_msg)
            except Exception as e:
                error_msg = f"OpenRouter request failed: {str(e)}"
                print(f"❌ [CHAT] {error_msg}")
                print(traceback.format_exc())
                raise ExternalServiceError(error_msg)
