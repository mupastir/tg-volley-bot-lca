from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    gemini_api_key: str
    gemini_model: str = "gemini-3.8-flash"
    tg_bot_token: str
    super_users: list[str] = []


load_dotenv()

settings = Settings()
