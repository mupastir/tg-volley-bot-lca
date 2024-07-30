import json
from asyncio import run
from typing import Any

from app.main import bot


def lambda_handler(event: dict, context: Any) -> dict:
    message = json.loads(event["body"])
    run(bot.async_handler(message))
    return {"statusCode": 200, "body": "OK"}
