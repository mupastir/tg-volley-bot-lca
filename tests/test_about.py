from unittest import mock
from unittest.mock import MagicMock

from minigram import MiniGramUpdate

from app.bot import Bot


@mock.patch("app.bot.Bot.req")
async def test_about_message(
    mock_req: MagicMock, minigram_update_about_message: MiniGramUpdate
) -> None:
    bot = Bot("token", mock.Mock())
    await bot.handle_update(minigram_update_about_message)

    assert "sendMessage" in mock_req.call_args.args
    assert mock_req.call_args.kwargs["chat_id"] == 1
    assert (
        mock_req.call_args.kwargs["reply_to_message_id"]
        == minigram_update_about_message.message_id
    )
    assert mock_req.call_args.kwargs["text"] is not None
    assert len(mock_req.call_args.kwargs["text"]) > 1
