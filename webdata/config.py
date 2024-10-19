import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)


class Settings(BaseSettings):
    """App settings."""
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    project_name: str = "webdata"
    debug: bool = True
    environment: str = "local"

    # Database
    DATABASE_URL: str = ""


settings = Settings()
