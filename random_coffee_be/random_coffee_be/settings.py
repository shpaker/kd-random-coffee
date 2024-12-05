from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from kd_random_coffee_utils.types import AppEnvironments


class AppSettings(
    BaseSettings,
):
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

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="kd_",
        env_file=".env",
    )


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
def get_app_settings() -> AppSettings:
    return AppSettings()


@lru_cache
def get_env_settings() -> EnvSettings:
    return EnvSettings()
# Класс AppSettings - создается класс, к нему импортируется BaseSettings, а он уже определяет настройки, связанные с приложением.
# Поля: описания их были закомментированы в файле set.env, кроме нескольких
# model_config: Конфигурация для загрузки настроек таких как: case_sensitive = False - означает что переменные окружения не будут чувствительны к регистру
# env_prefix = "kd_" - обычный префикс для переменных окружения например KD_DATABASE_URL
# env_file = ".env": Файл из которого будут загружены переменные окружения.
# Класс EnvSettings - создается класс, к нему импортируется BaseSettings, а он определяет настройки, связанные с окружением приложения.
# Поля: app_environment - окружение приложения например у нас в файле set.env стоит development то есть в разработке
# app_version - версия приложения
# model_config аналогичен тому что было в классе AppSettings
# Функция get_app_settings - эта функция нужна для кэширования результата вызова AppSettings(), то есть при первом вызове функции будет создан экземпляр AppSetting,
# а при последующих будет возвращен кэшированный вариант.
# Функция get_env_settings - аналогично первой функции
# Ну и если рассматривать для чего нужен этот файл, то как я понял он может предоставить удобный способ загрузки и управления настройками приложения, 
# а использование pydantic позволит легко валидировать(процесс проверки файлов в соответствии определенным правилам и требованиям) и загружать настройки из переменных окружения
# также с помощью lru_cache обеспечить повторное использование настроек без дополнительной загрузки. 