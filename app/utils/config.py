from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache

#base class for all the env variables

class Config(BaseSettings):
    DB_URL:str

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
        case_sensitive=False,
        use_enum_values=True,
    )

@lru_cache
def get_settings() -> Config:
    return Config()