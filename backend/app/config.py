from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+asyncpg://habitopro:habitopro@db:5432/habitopro"

    ai_provider: str = "claude"
    anthropic_api_key: str = ""
    claude_model: str = "claude-opus-5"

    whatsapp_verify_token: str = ""
    whatsapp_access_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_api_version: str = "v21.0"


settings = Settings()
