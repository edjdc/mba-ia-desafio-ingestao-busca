from enum import Enum
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class LLMProvider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"

class Settings(BaseSettings):
    DATABASE_URL: str

    LLM_PROVIDER: LLMProvider

    OPENAI_API_KEY: str | None = None
    OPENAI_BASE_URL: str | None = None
    GOOGLE_API_KEY: str | None = None

    OPENAI_EMBEDDING_MODEL: str
    OPENAI_LLM_MODEL: str

    GEMINI_EMBEDDING_MODEL: str
    GEMINI_LLM_MODEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @model_validator(mode='after')
    def auto_configure_provider(self):
        if self.OPENAI_API_KEY:
            pass
        elif self.GOOGLE_API_KEY:
             self.LLM_PROVIDER = LLMProvider.GEMINI
        else:
             raise ValueError("Nenhuma chave de API encontrada (OPENAI_API_KEY ou GOOGLE_API_KEY). Verifique seu arquivo .env.")
        
        return self

settings = Settings()
