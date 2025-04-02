from unittest import mock
from unittest.mock import MagicMock
from app import MiniGramUpdate
from app.bot import Bot


@mock.patch("app.bot.Bot.req")
async def test_translate_from_ukr_msg(
    mock_req: MagicMock, minigram_en_msg: MiniGramUpdate
) -> None:
    bot = Bot("token", mock.AsyncMock(), ["mupastir"])
    await bot.handle_update(minigram_en_msg)

    mock_req.assert_not_called()
