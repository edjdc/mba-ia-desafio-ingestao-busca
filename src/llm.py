from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from src.config import settings, LLMProvider

def get_embeddings():
    if settings.LLM_PROVIDER == LLMProvider.OPENAI:
        params = {
            "base_url": settings.OPENAI_BASE_URL,
            "model": settings.OPENAI_EMBEDDING_MODEL,
            "api_key": settings.OPENAI_API_KEY,
        }
        return OpenAIEmbeddings(**{k: v for k, v in params.items() if v is not None})
    
    elif settings.LLM_PROVIDER == LLMProvider.GEMINI:
        return GoogleGenerativeAIEmbeddings(
            model=settings.GEMINI_EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )
    else:
        raise ValueError(f"Unsupported provider: {settings.LLM_PROVIDER}")

def get_llm():
    if settings.LLM_PROVIDER == LLMProvider.OPENAI:
        params = {
            "base_url": settings.OPENAI_BASE_URL,
            "model": settings.OPENAI_LLM_MODEL,
            "api_key": settings.OPENAI_API_KEY,
            "temperature": 0,
        }
        return ChatOpenAI(**{k: v for k, v in params.items() if v is not None})
    
    elif settings.LLM_PROVIDER == LLMProvider.GEMINI:
        return ChatGoogleGenerativeAI(
            model=settings.GEMINI_LLM_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0
        )
    else:
        raise ValueError(f"Unsupported provider: {settings.LLM_PROVIDER}")
