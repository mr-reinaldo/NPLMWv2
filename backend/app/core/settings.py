from pydantic_settings import BaseSettings
from pydantic import BaseModel, PostgresDsn, AmqpDsn, PositiveInt
from pydantic.networks import IPvAnyAddress
from decouple import config as env_config


env_config.encoding = "utf-8"


class APISettings(BaseModel):
    server_host: IPvAnyAddress = env_config(
        "API_SERVER_HOST", cast=str, default="0.0.0.0"
    )
    server_port: PositiveInt = env_config("API_SERVER_PORT", cast=int, default=8000)
    api_prefix: str = "/api/v1"


class JWTSettings(BaseModel):
    secret_key: str = env_config("API_JWT_SECRET_KEY", cast=str)
    algorithm: str = env_config("API_JWT_ALGORITHM", cast=str)
    expire_minutes: int = env_config("API_JWT_EXPIRE_MINUTES", cast=int)


class DatabaseSettings(BaseModel):
    url: PostgresDsn = env_config("DATABASE_URL", cast=str)
    echo: bool = env_config("DATABASE_ECHO", cast=bool)


# class CelerySettings(BaseModel):
#     broker_url: AmqpDsn = env_config("CELERY_BROKER_URL", cast=str)
#     result_backend: PostgresDsn = env_config("CELERY_RESULT_BACKEND", cast=str)


class Settings(BaseSettings):
    api: APISettings = APISettings()
    jwt: JWTSettings = JWTSettings()
    database: DatabaseSettings = DatabaseSettings()
    # celery: CelerySettings = CelerySettings()


settings = Settings()
