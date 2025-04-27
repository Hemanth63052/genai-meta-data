import os

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from scripts.utils.gcp_secret_manager import get_gcp_secrets

load_dotenv()

class _ServerConfig(BaseSettings):
    """
    Server configuration settings.
    """

    SERVER_HOST: str = Field(default="0.0.0.0")
    SERVER_PORT: int = Field(default=6305)

class _LoggingConfig(BaseSettings):
    """
    Logging configuration settings.
    """

    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: str = Field(default="logs/app.log")
    LOG_FORMAT: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    LOG_DATE_FORMAT: str = Field(default="%Y-%m-%d %H:%M:%S")

class _MongoDBConfig(BaseSettings):
    """
    MongoDB configuration settings.
    """

    MONGODB_URI: str

class _RedisConfig(BaseSettings):
    """
    Redis configuration settings.
    """

    REDIS_URI: str

class _JWTConfig(BaseSettings):
    """
    JWT configuration settings.
    """

    PUBLIC_KEY: str | None = None
    PRIVATE_KEY: str | None = None
    JWT_ALGORITHM: str = "RS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24)  # give it for 1 day
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24 * 7)  # 7 days

    @model_validator(mode="before")
    def validate_keys(cls, values):
        if not values.get("PUBLIC_KEY") or not values.get("PRIVATE_KEY"):
            project_name = os.environ.get("GCP_PROJECT_NAME", 'adaptiq-457516')
            get_rsa_public_key = get_gcp_secrets("rsa-public-key", project_name)
            get_rsa_private_key = get_gcp_secrets("rsa-private-key", project_name)
            if get_rsa_public_key and get_rsa_private_key:
                values["PUBLIC_KEY"] = get_rsa_public_key
                values["PRIVATE_KEY"] = get_rsa_private_key
        return values


ServerConfig = _ServerConfig()
LoggingConfig = _LoggingConfig()
MongoDBConfig = _MongoDBConfig()
RedisConfig = _RedisConfig()
JWTConfig = _JWTConfig()


__all__ = ["ServerConfig", "MongoDBConfig", "RedisConfig", "JWTConfig", "LoggingConfig"]
