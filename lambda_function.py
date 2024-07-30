import json
from typing import Any

from app.main import bot


async def lambda_handler(event: dict, context: Any) -> None:
    message = json.loads(event["body"])
    await bot.handle_update(message)
