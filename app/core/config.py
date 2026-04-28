# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    APP_NAME: str = Field(default="llm-p")
    ENV: str = Field(default="local")
    
    JWT_SECRET: str = Field(default="change_me_super_secret")
    JWT_ALG: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    
    SQLITE_PATH: str = Field(default="./app.db")
    
    OPENROUTER_API_KEY: str = Field(default="")
    OPENROUTER_BASE_URL: str = Field(default="https://openrouter.ai/api/v1")
    OPENROUTER_MODEL: str = Field(default="stepfun/step-3.5-flash:free")
    OPENROUTER_SITE_URL: str = Field(default="https://example.com")
    OPENROUTER_APP_NAME: str = Field(default="llm-fastapi-openrouter")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
