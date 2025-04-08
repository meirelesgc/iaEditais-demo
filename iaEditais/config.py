from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API: str = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
