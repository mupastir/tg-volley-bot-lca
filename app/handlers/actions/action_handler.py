from typing import TYPE_CHECKING

from app.handlers.actions.ask_ai_handler import AI_MODIFIERS, ask_ai_handler
from app.handlers.actions.exceptions import ActionNotRecognized
from app.handlers.actions.translate import translate_handler

if TYPE_CHECKING:
    from app.bot import Bot


async def handle_action(bot: "Bot", message: str, user: dict) -> str:
    if any(message.startswith(modifier) for modifier in AI_MODIFIERS):
        return await ask_ai_handler(
            llm=bot.llm,
            question=message,
            user=user,
            super_users=bot.super_users,
        )

    translated_text = translate_handler(message)
    if translated_text:
        return translated_text
    raise ActionNotRecognized()
