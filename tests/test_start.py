from unittest import mock
from unittest.mock import MagicMock

from minigram import MiniGramUpdate

from app.bot import Bot


@mock.patch("app.bot.Bot.req")
async def test_start_message(
    mock_req: MagicMock, minigram_update_start_message: MiniGramUpdate
) -> None:
    bot = Bot("token", mock.AsyncMock(), ["mupastir"])
    await bot.handle_update(minigram_update_start_message)

    mock_req.assert_called_once_with(
        "sendMessage",
        chat_id=1,
        reply_to_message_id=minigram_update_start_message.message_id,
        text="Hello. I am an bot assistance for beach volleyball chat! 👋\nPress /help to see available commands.",
    )
