from pydantic_settings import BaseSettings, SettingsConfigDict


class FastAPIConfig(BaseSettings):
    host: str
    port: int
    reload: bool

    model_config = SettingsConfigDict(env_prefix='server_', env_file=".env", env_file_encoding="utf-8")

