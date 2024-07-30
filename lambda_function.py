import json
from asyncio import get_event_loop
from typing import Any

from app.main import bot


def lambda_handler(event: dict, context: Any) -> dict:
    message = json.loads(event["body"])
    loop = get_event_loop()
    loop.run_until_complete(bot.async_handler(message))
    return {"statusCode": 200, "body": "OK"}
