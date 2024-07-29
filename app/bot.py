from minigram import StarletteMiniGram, MiniGramUpdate

from logging import getLogger

from app.gateways.openai import OpenAI, OpenAIError
from app.handlers.help import help_handler


logger = getLogger(__name__)


class Bot(StarletteMiniGram):
    def __init__(self, key: str, openai_: OpenAI) -> None:
        super().__init__(key)
        self.openai = openai_

    async def handle_update(self, update: MiniGramUpdate) -> None:
        result: str = "I don't understand you 😔"

        match update.text:
            case "/start":
                result = "Hello from Starlette! 👋"
            case "/help":
                result = help_handler()
            case "ping":
                result = "pong"
            case "ai!" | "gpt!" | "openai!" | "чат!":
                try:
                    result = await self.openai.easy_complete(
                        "What’s on your mind?",
                        "You are a chat bot of beach volleyball community.",
                    )
                except OpenAIError as e:
                    logger.error("Failed to get AI response.", exc_info=e)

            case _:
                if not update.text.startswith("/"):
                    return None

        await self.reply(update, result)
