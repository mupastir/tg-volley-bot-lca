from app import AsyncMiniGram, MiniGramUpdate

from logging import getLogger

from app.gateways.openai import OpenAI, OpenAIError
from app.handlers.help import help_handler
from app.handlers.about_handler import about_handler
from app.handlers.actions.exceptions import ActionNotRecognized
from app.handlers.actions.action_handler import handle_action

logger = getLogger(__name__)


class Bot(AsyncMiniGram):
    def __init__(self, key: str, openai_: OpenAI, super_users: list[str]) -> None:
        super().__init__(key)
        self.openai = openai_
        self.super_users = tuple(super_users)

    async def handle_update(self, update: MiniGramUpdate) -> None:
        result: str = "I don't understand you 😔"

        if update.text is None or update.from_user.get("is_bot"):
            logger.warning("Received message.", extra={"update": update})
            return

        match update.text:
            case "/start":
                result = (
                    "Hello. I am an bot assistance for beach volleyball chat! 👋\n"
                    "Press /help to see available commands."
                )
            case "/help":
                result = help_handler()
            case "fact!" | "oneliner!":
                result = about_handler()
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
                if update.text.startswith("/"):
                    logger.info("Command not recognized.", extra={"text": update.text})
                    await self.reply(update, result)
                    return None
                try:
                    result = await handle_action(self, update.text, update.from_user)
                except ActionNotRecognized:
                    logger.info("Action not recognized.", extra={"text": update.text})
                    return None

        await self.reply(update, result)
