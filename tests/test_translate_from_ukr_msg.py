from unittest import mock
from unittest.mock import MagicMock
from app import MiniGramUpdate
from app.bot import Bot


@mock.patch("app.bot.Bot.req")
async def test_translate_from_ukr_msg(
    mock_req: MagicMock, minigram_ukr_msg: MiniGramUpdate
) -> None:
    bot = Bot("token", mock.AsyncMock(), ["mupastir"])
    await bot.handle_update(minigram_ukr_msg)

    mock_req.assert_called_once_with(
        "sendMessage",
        chat_id=1,
        reply_to_message_id=minigram_ukr_msg.message_id,
        text="<i> Let's play with Misha's Ball </i>",
    )
