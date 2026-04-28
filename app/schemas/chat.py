# app/schemas/chat.py
from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    system: Optional[str] = Field(default=None)
    max_history: int = Field(default=10, ge=0, le=50)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    answer: str


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: str
    
    model_config = ConfigDict(from_attributes=True)
