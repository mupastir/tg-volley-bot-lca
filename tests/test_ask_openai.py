from datetime import datetime
from unittest import mock
from unittest.mock import MagicMock
from uuid import uuid4

from app import MiniGramUpdate

from app.bot import Bot
from app.models.openai.record import UserQuestionRecord
from app.models.openai.response import Answer


@mock.patch("app.handlers.actions.ask_ai_handler.get_last_messages")
@mock.patch("app.handlers.actions.ask_ai_handler.save_new_message")
@mock.patch("app.bot.Bot.req")
async def test_ask_openai_message_with_no_history(
    mock_req: MagicMock,
    save_new_message: MagicMock,
    get_last_messages: MagicMock,
    minigram_update_ask_openai_message: MiniGramUpdate,
) -> None:
    bot = Bot("token", mock.AsyncMock(), [])
    get_last_messages.return_value = []
    bot.openai.easy_complete.return_value = "Answer from OpenAI"
    await bot.handle_update(minigram_update_ask_openai_message)

    bot.openai.easy_complete.assert_called_once_with(
        "How to serve skyball?",
        (
            "You are a chatbot from the beach volleyball community in Larnaca, Cyprus. "
            "You have an excellent sense of humor and your favorite genre is pun jokes. "
            "Meanwhile, you have outstanding knowledge in sports, nutrition, sports psychology, "
            "and connected areas to beach volleyball. "
            "You answer with no more than 50 words, should be in English language."
        ),
        temperature=1.1,
    )
    save_new_message.assert_called_once()
    mock_req.assert_called_once_with(
        "sendMessage",
        chat_id=1,
        reply_to_message_id=minigram_update_ask_openai_message.message_id,
        text="Answer from OpenAI",
    )


@mock.patch("app.handlers.actions.ask_ai_handler.get_last_messages")
@mock.patch("app.handlers.actions.ask_ai_handler.save_new_message")
@mock.patch("app.bot.Bot.req")
async def test_ask_openai_message_with_history(
    mock_req: MagicMock,
    save_new_message: MagicMock,
    get_last_messages: mock.AsyncMock,
    minigram_update_ask_openai_message: MiniGramUpdate,
    openai_response: Answer,
) -> None:
    bot = Bot("token", mock.AsyncMock(), [])
    get_last_messages.return_value = [
        UserQuestionRecord(
            id=uuid4(),
            user_id=1,
            question="How to serve skyball?",
            answer="Skyball is a serve that is hit with the knuckles",
            created_at=datetime.now(),
            expires_at=1700000,
        )
    ]
    bot.openai.complete.return_value = openai_response
    await bot.handle_update(minigram_update_ask_openai_message)

    bot.openai.complete.assert_called_once()
    bot.openai.easy_complete.assert_not_called()
    save_new_message.assert_called_once()
    mock_req.assert_called_once_with(
        "sendMessage",
        chat_id=1,
        reply_to_message_id=minigram_update_ask_openai_message.message_id,
        text="Answer from OpenAI",
    )


@mock.patch("app.handlers.actions.ask_ai_handler.get_last_messages")
@mock.patch("app.handlers.actions.ask_ai_handler.save_new_message")
@mock.patch("app.bot.Bot.req")
async def test_ask_openai_message_with_history_reached_limits(
    mock_req: MagicMock,
    save_new_message: MagicMock,
    get_last_messages: mock.AsyncMock,
    minigram_update_ask_openai_message: MiniGramUpdate,
    openai_response: Answer,
) -> None:
    bot = Bot("token", mock.AsyncMock(), [])
    get_last_messages.return_value = [
        UserQuestionRecord(
            id=uuid4(),
            user_id=1,
            question="How to serve skyball?",
            answer="Skyball is a serve that is hit with the knuckles",
            created_at=datetime.now(),
            expires_at=1700000,
        )
        for _ in range(10)
    ]
    bot.openai.complete.return_value = openai_response
    await bot.handle_update(minigram_update_ask_openai_message)

    bot.openai.complete.assert_not_called()
    bot.openai.easy_complete.assert_not_called()
    save_new_message.assert_not_called()
    mock_req.assert_called_once_with(
        "sendMessage",
        chat_id=1,
        reply_to_message_id=minigram_update_ask_openai_message.message_id,
        text="You have reached the limit of 5 questions per day. "
        "Please wait some time maybe your limit would be updated soon.",
    )


@mock.patch("app.handlers.actions.ask_ai_handler.get_last_messages")
@mock.patch("app.handlers.actions.ask_ai_handler.save_new_message")
@mock.patch("app.bot.Bot.req")
async def test_ask_openai_message_with_history_reached_limits_as_superuser(
    mock_req: MagicMock,
    save_new_message: MagicMock,
    get_last_messages: mock.AsyncMock,
    minigram_update_ask_openai_message: MiniGramUpdate,
    openai_response: Answer,
) -> None:
    bot = Bot("token", mock.AsyncMock(), ["testuser"])
    get_last_messages.return_value = [
        UserQuestionRecord(
            id=uuid4(),
            user_id=1,
            question="How to serve skyball?",
            answer="Skyball is a serve that is hit with the knuckles",
            created_at=datetime.now(),
            expires_at=1700000,
        )
        for _ in range(10)
    ]
    bot.openai.complete.return_value = openai_response
    await bot.handle_update(minigram_update_ask_openai_message)

    bot.openai.complete.assert_called_once()
    bot.openai.easy_complete.assert_not_called()
    save_new_message.assert_called_once()
    mock_req.assert_called_once_with(
        "sendMessage",
        chat_id=1,
        reply_to_message_id=minigram_update_ask_openai_message.message_id,
        text="Answer from OpenAI",
    )


@mock.patch("app.handlers.actions.ask_ai_handler.get_last_messages")
@mock.patch("app.handlers.actions.ask_ai_handler.save_new_message")
@mock.patch("app.bot.Bot.req")
async def test_ask_openai_short_message(
    mock_req: MagicMock,
    save_new_message: MagicMock,
    get_last_messages: mock.AsyncMock,
    minigram_update_ask_openai_short_message: MiniGramUpdate,
    openai_response: Answer,
) -> None:
    bot = Bot("token", mock.AsyncMock(), ["mupastir"])
    bot.openai.complete.return_value = openai_response
    await bot.handle_update(minigram_update_ask_openai_short_message)

    bot.openai.complete.assert_not_called()
    bot.openai.easy_complete.assert_not_called()
    get_last_messages.assert_not_called()
    save_new_message.assert_not_called()
    mock_req.assert_called_once_with(
        "sendMessage",
        chat_id=1,
        reply_to_message_id=minigram_update_ask_openai_short_message.message_id,
        text="Please ask a more specific question. "
        "Maybe your question is too short or contains a word that is not allowed.",
    )
