# app/config.py

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PORT: int = 8000
    HOST: str = "localhost"
    OPENAI_API_KEY: str
    REDIST_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    env = os.getenv("ENV", "local")  # e.g., prd, tst, local
    env_file = f".env.{env}" if env in {"prd", "tst"} else ".env"
    Settings.Config.env_file = env_file
    return Settings()
