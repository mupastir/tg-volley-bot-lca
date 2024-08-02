from unittest import mock
from unittest.mock import MagicMock

from app import MiniGramUpdate

from app.bot import Bot


@mock.patch("app.bot.Bot.req")
async def test_help_message(
    mock_req: MagicMock, minigram_update_help_message: MiniGramUpdate
) -> None:
    bot = Bot("token", mock.AsyncMock(), ["mupastir"])
    await bot.handle_update(minigram_update_help_message)

    mock_req.assert_called_once_with(
        "sendMessage",
        chat_id=1,
        reply_to_message_id=minigram_update_help_message.message_id,
        text="fact!, oneliner! - to get any random fact about Oleh "
        "or about volleyball or something else\n"
        "ping - respond pong\n"
        "ai!, gpt!, openai!, чат! - to ask a question to the AI, for example: *ai! How to serve skyball?*\n"
        "rules? - Know the measure and do not force the bot. "
        "If you received a warning *there are too many of you...* "
        "- do not continue and create noise. "
        "This is a boto-ban and it will pass itself in 15 minutes "
        "if you are not active. For those for whom this soft ban "
        "is not enough, there is also a super-duper ban, "
        "so *don't go to extremes*. "
        "You can communicate with the bot directly through "
        "private messages.",
    )
