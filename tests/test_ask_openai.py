from unittest import mock
from unittest.mock import MagicMock

from minigram import MiniGramUpdate

from app.bot import Bot


@mock.patch("app.bot.Bot.req")
async def test_ask_openai_message(
    mock_req: MagicMock, minigram_update_ask_openai_message: MiniGramUpdate
) -> None:
    bot = Bot("token", mock.AsyncMock())
    bot.openai.easy_complete.return_value = "Answer from OpenAI"
    await bot.handle_update(minigram_update_ask_openai_message)

    bot.openai.easy_complete.assert_called_once_with(
        "How to serve skyball?",
        (
            "You are a chat bot of beach volleyball community. "
            "You answer with no more than 50 words, should be in English language"
        ),
    )
    mock_req.assert_called_once_with(
        "sendMessage",
        chat_id=1,
        reply_to_message_id=minigram_update_ask_openai_message.message_id,
        text="Answer from OpenAI",
    )
