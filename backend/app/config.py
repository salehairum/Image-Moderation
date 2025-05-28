from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str

    class Config:
        env_file = ".env"  # Optional fallback, Compose env vars take priority
        env_file_encoding = "utf-8"


settings = Settings()
