from app.bot import Bot
from app.gateways.openai import OpenAI

from app.settings import settings

openai = OpenAI(settings.openai_api_key, model=settings.openai_model)
bot = Bot(settings.tg_bot_token, openai, settings.super_users)
