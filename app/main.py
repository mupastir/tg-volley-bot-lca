from app.bot import Bot
from app.gateways.gemini import Gemini
from app.settings import settings

gemini = Gemini(settings.gemini_api_key, model=settings.gemini_model)
bot = Bot(settings.tg_bot_token, gemini, settings.super_users)
