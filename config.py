"""
Configuration module for AI Humanizer application.
Handles environment variables and application settings.
"""
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Ollama Configuration
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama2")
    
    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # AI Humanizer Configuration
    max_text_length: int = int(os.getenv("MAX_TEXT_LENGTH", "10000"))
    min_text_length: int = int(os.getenv("MIN_TEXT_LENGTH", "10"))
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "60"))
    
    class Config:
        env_file = ".env"


settings = Settings()
