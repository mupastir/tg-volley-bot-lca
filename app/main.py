from starlette.applications import Starlette
from starlette.routing import Route

from bot import Bot
from gateways.openai import OpenAI
from settings import settings

openai = OpenAI(settings.openai_api_key, model=settings.openai_model)
bot = Bot(settings.tg_bot_token, openai)
bot.set_webhook("https://yourwebsite.com/webhook")

app = Starlette(
    debug=settings.debug,
    routes=[
        Route("/webhook", bot.starlette_handler, methods=["POST"]),
    ],
)
