from pydantic_settings import BaseSettings, SettingsConfigDict

origins = [
    "*"
]


class FastAPIConfig(BaseSettings):
    host: str
    port: int
    reload: bool

    model_config = SettingsConfigDict(env_prefix='server_', env_file=".env", env_file_encoding="utf-8")


class RedisConfig(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix="redis_", env_file=".env", env_file_encoding="utf-8")


class DbConfig(BaseSettings):
    service: str
    user: str
    password: str
    name: str
    domain: str
    port: int
    url: str

    model_config = SettingsConfigDict(env_prefix="postgres_", env_file=".env", env_file_encoding="utf-8")
