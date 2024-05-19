from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    ADMIN_PIN: str
    TELEGRAM_USERNAME: str
    WHATSAPP_NUMBER: str

    FRONTEND_SALE_END: str | None = None

settings = Settings()