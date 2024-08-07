from uuid import uuid4

import aioboto3
from datetime import datetime, timedelta

from boto3.dynamodb.conditions import Attr

from app.gateways.openai import OpenAI
from app.models.openai.record import UserQuestionRecord
from app.models.openai.request import Message

OPENAI_MODIFIERS = (
    "ai!",
    "gpt!",
    "openai!",
    "чат!",
)
SYSTEM_PROMPT = (
    "You are a chatbot from the beach volleyball community in Larnaca, Cyprus. "
    "You have an excellent sense of humor and your favorite genre is pun jokes. "
    "Meanwhile, you have outstanding knowledge in sports, nutrition, sports psychology, "
    "and connected areas to beach volleyball. "
    "You answer with no more than 50 words, should be in English language."
)

aioboto_session = aioboto3.Session()


async def ask_ai_handler(
    openai_: OpenAI,
    question: str,
    user: dict,
    super_users: tuple[str, ...] | None = None,
) -> str:
    q = question.split("!", 1)[1].strip()
    if len(q) < 5 or "idle" in q:  # do not respond on too short questions or idle
        return (
            "Please ask a more specific question. "
            "Maybe your question is too short or contains a word that is not allowed."
        )
    now = datetime.now()
    one_day_before = now - timedelta(days=1)

    user_last_messages = await get_last_messages(user["id"])
    user_last_day_messages = [
        message
        for message in user_last_messages
        if message.created_at >= one_day_before
    ]
    if len(user_last_day_messages) >= 5 and user["username"] not in super_users:
        return (
            "You have reached the limit of 5 questions per day. "
            "Please wait some time maybe your limit would be updated soon."
        )

    if user_last_day_messages:
        messages = [Message(role="system", content=SYSTEM_PROMPT)]
        for message in user_last_messages[:15]:  # provide last 15 messages into chat
            messages.append(Message(role="user", content=message.question))
            messages.append(Message(role="assistant", content=message.answer))
        messages.append(Message(role="user", content=q))

        answer = await openai_.complete(
            messages=messages, max_tokens=1000, temperature=1.1
        )
        if not answer.choices:
            return "No response from OpenAI"
        result_message = answer.choices[0].message.content
    else:
        result_message = await openai_.easy_complete(
            q,
            SYSTEM_PROMPT,
            temperature=1.1,  # type: ignore
        )

    await save_new_message(
        UserQuestionRecord(
            id=uuid4(),
            user_id=user["id"],
            question=q,
            answer=result_message,
            created_at=now,
            expires_at=int((now + timedelta(days=5)).timestamp()),
        )
    )
    return result_message


async def get_last_messages(user_id: int) -> list[UserQuestionRecord]:
    async with aioboto_session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("tg_volley_bot_openai_requests")
        response = await table.scan(FilterExpression=Attr("user_id").eq(user_id))
    return [UserQuestionRecord(**item) for item in response["Items"]]


async def save_new_message(question_record: UserQuestionRecord) -> None:
    async with aioboto_session.resource("dynamodb") as dynamodb:
        table = await dynamodb.Table("tg_volley_bot_openai_requests")
        await table.put_item(Item=question_record.model_dump(mode="json"))
