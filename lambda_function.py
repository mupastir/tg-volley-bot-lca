import json
from asyncio import get_event_loop
from typing import Any

from langfuse import get_client

from app.main import bot


def lambda_handler(event: dict, context: Any) -> dict:
    message = json.loads(event["body"])
    loop = get_event_loop()
    try:
        loop.run_until_complete(bot.async_handler(message))
    finally:
        # Lambda may freeze the process right after returning, so export traces synchronously.
        get_client().flush()
    return {"statusCode": 200, "body": "OK"}
