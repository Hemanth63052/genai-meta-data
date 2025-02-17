from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

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

    PUBLIC_KEY_PATH: str | None = None
    PRIVATE_KEY_PATH: str | None = None
    JWT_ALGORITHM: str = "RSA256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=10)


ServerConfig = _ServerConfig()
LoggingConfig = _LoggingConfig()
MongoDBConfig = _MongoDBConfig()
RedisConfig = _RedisConfig()
JWTConfig = _JWTConfig()


__all__ = ["ServerConfig", "MongoDBConfig", "RedisConfig", "JWTConfig", "LoggingConfig"]
