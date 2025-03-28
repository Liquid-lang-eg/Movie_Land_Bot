from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    DOCKER_HUB_USERNAME: str
    BOT_TOKEN: str

    SECRET_KEY_ADMIN: str
    ALGORITHM: str = "HS256"

    TMDB_API_KEY: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: str

    MAX_ERROR_LENGTH: int = 500

    BACKEND_URL: str

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
