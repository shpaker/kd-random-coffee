from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum

class AppEnvironments(Enum):
    LOCAL = "local"
    PROD = "prod"

class AppSettings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_expiration: int
    app_port: int
    telegram_bot_token: str
    email_sender: str
    email_smtp_server: str
    email_smtp_port: int
    email_username: str
    email_password: str
    external_api_base_url: str
    external_api_token: str
    app_environment: AppEnvironments
    app_version: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="kd_",
        env_file=".env",
    )

@lru_cache
def get_app_settings() -> AppSettings:
    settings = AppSettings()
    print(settings)  # Добавьте это для отладки
    return settings

class EnvSettings(BaseSettings):
    app_environment: AppEnvironments
    app_version: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="kd_",
        env_file=".env",
    )

@lru_cache
def get_env_settings() -> AppSettings:  # Исправлено на AppSettings
    settings = AppSettings()
    print(settings)  # Добавьте это для отладки
    return settings