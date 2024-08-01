from typing import TYPE_CHECKING

from app.handlers.actions.ask_ai_handler import OPENAI_MODIFIERS, ask_ai_handler
from app.handlers.actions.exceptions import ActionNotRecognized

if TYPE_CHECKING:
    from app.bot import Bot


async def handle_action(bot: "Bot", message: str, user: dict) -> str:
    if any(message.startswith(modifier) for modifier in OPENAI_MODIFIERS):
        return await ask_ai_handler(
            openai_=bot.openai, question=message, user=user, super_users=bot.super_users
        )
    raise ActionNotRecognized()
