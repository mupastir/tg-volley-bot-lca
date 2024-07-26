from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    openai_api_key: str
    openai_model: str
    tg_bot_token: str


load_dotenv()
settings = Settings()
