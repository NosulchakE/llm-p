# app/services/openrouter_client.py
import httpx
from typing import List, Dict

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
    
    async def chat_completion(self, messages: List[Dict[str, str]]) -> str:
        """Отправка запроса к OpenRouter"""
        
        # Проверка наличия API ключа
        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            raise ExternalServiceError("OpenRouter API key is not configured")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_APP_NAME,
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    follow_redirects=True,  # ✅ важно для обработки 307
                )
                
                if response.status_code == 401:
                    raise ExternalServiceError("OpenRouter: Invalid API key")
                elif response.status_code == 429:
                    raise ExternalServiceError("OpenRouter: Rate limit exceeded")
                elif response.status_code != 200:
                    raise ExternalServiceError(f"OpenRouter error: {response.status_code} - {response.text}")
                
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
            except httpx.TimeoutException:
                raise ExternalServiceError("OpenRouter timeout after 60 seconds")
            except httpx.ConnectError:
                raise ExternalServiceError("Cannot connect to OpenRouter. Check network/proxy settings")
            except Exception as e:
                raise ExternalServiceError(f"OpenRouter request failed: {str(e)}")
