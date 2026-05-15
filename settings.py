from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    data_dir: str = "./data"
    title: str = "Hi-CService"

    class Config:
        env_file = ".env"
