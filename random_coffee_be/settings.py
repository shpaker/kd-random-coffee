from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from kd_random_coffee_utils.types import AppEnvironments


class AppSettings(
    BaseSettings,
): ...


class EnvSettings(
    BaseSettings,
):
    app_environment: AppEnvironments
    app_version: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="kd_",
        env_file=".env",
    )


@lru_cache
def get_at_settings() -> AppSettings:
    return AppSettings()


@lru_cache
def get_env_settings() -> EnvSettings:
    return EnvSettings()
