from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_pass: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_expire: int

    class Config:
        env_file=".env"


settings=Settings()