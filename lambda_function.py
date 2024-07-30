import json
from typing import Any

from app.main import bot


def lambda_handler(event: dict, context: Any) -> None:
    message = json.loads(event["body"])
    from asyncio import gather, get_event_loop

    loop = get_event_loop()
    loop.run_until_complete(gather(bot.async_handler(message)))
    loop.close()
