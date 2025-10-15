from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    use_openai: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

