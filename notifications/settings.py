from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    email_user: str
    email_host: str
    email_port: int
    email_password: str
    email_receiver: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
