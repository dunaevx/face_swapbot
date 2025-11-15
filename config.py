# config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    bot_token: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_pass: str = "lol69056"
    db_name: str = "face_swap_db"
    face_swap_api_url: str
    face_swap_api_key: str = ""
    webapp_url: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

config = Settings()