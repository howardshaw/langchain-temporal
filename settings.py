from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Langchain Tempral Service"
    # FastAPI 配置
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: List[str] = ["*"]

    TEMPORAL_HOST: str = "localhost"
    REDIS_HOST: str = "localhost"
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai-hk.com/v1"
    OPENAI_MODEL: str = ""

    class Config:
        env_file = ".env"
        extra = "allow"
        case_sensitive = False


# 创建全局设置实例
settings = Settings()
