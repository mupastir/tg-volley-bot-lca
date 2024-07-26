from minigram import StarletteMiniGram, MiniGramUpdate
from starlette.applications import Starlette
from starlette.routing import Route

from gateways.openai import OpenAI
from settings import settings


class MyStarletteBot(StarletteMiniGram):
    def __init__(self):
        super().__init__(settings.tg_bot_token)
        self.openai_bot = OpenAI(settings.openai_api_key, model=settings.openai_model)

    async def handle_update(self, update: MiniGramUpdate) -> dict:
        result: str
        match update.text:
            case "/start":
                result = "Hello from Starlette! 👋"
            case "ai!" | "gpt!" | "openai!" | "чат!":
                result = await self.openai_bot.easy_complete(
                    "What’s on your mind?",
                    "You are a chat bot of beach volleyball community.",
                )
            case _:
                result = "I don't understand you 😔"

        print(f"Result: {result}")
        return await self.reply(update, result)


bot = MyStarletteBot()
bot.set_webhook("https://yourwebsite.com/webhook")

app = Starlette(
    debug=settings.debug,
    routes=[
        Route("/webhook", bot.starlette_handler, methods=["POST"]),
    ],
)
