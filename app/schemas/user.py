# app/schemas/user.py
from pydantic import BaseModel, ConfigDict


class UserPublic(BaseModel):
    id: int
    email: str
    role: str
    
    model_config = ConfigDict(from_attributes=True)
