from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache
import os
from pathlib import Path
#base class for all the env variables
env_file = Path(__file__).resolve().parent.parent/".env"
class Config(BaseSettings):
    DB_URL:str = os.environ.get('DB_URL')
    PORT:int = os.environ.get('PORT')
    HOST:str = os.environ.get('HOST')

    model_config=SettingsConfigDict(
        env_file=".env" if os.path.exists('.env') else env_file,
        env_file_encoding="utf-8",
        extra="allow",
        case_sensitive=False,
        use_enum_values=True,
    )

@lru_cache
def get_settings() -> Config:
    return Config()