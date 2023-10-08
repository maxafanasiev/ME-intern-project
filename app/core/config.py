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

    model_config = SettingsConfigDict(env_prefix="postgres_", env_file=".env", env_file_encoding="utf-8",
                                      extra="ignore")


class JWTConfig(BaseSettings):
    secret_key: str
    algorithm: str

    model_config = SettingsConfigDict(env_prefix="jwt_", env_file=".env", env_file_encoding="utf-8")


class AUTH0Config(BaseSettings):
    domain: str
    api_audience: str
    algorithm: str
    issuer: str
    secret_key: str

    model_config = SettingsConfigDict(env_prefix="auth0_", env_file=".env", env_file_encoding="utf-8")
