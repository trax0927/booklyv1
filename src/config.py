import sys
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    REDIS_URL: str = "redis://localhost:6379/0"
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    MAIL_PORT:int
    MAIL_SERVER:str
    MAIL_FROM_NAME:str
    MAIL_STARTTLS:bool =True
    MAIL_SSL_TLS:bool =False
    USE_CREDENTIALS:bool =True
    VALIDATE_CERTS:bool =True
    DOMAIN_NAME: str
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "testser"]

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()

broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL
broker_connection_retry_on_startup = True

# Celery's default prefork pool is not supported on Windows
if sys.platform == "win32":
    worker_pool = "solo"
