from unittest import mock
from unittest.mock import MagicMock

import pytest

from app.bot import Bot
from tests.helpers import get_update_event

message_cases = [
    "Ας παίξουμε με την μπάλα του Μίσα",
    "Let's play with Misha's ball",
]


@pytest.mark.parametrize("text", message_cases)
@mock.patch("app.bot.Bot.req")
async def test_translate_from_msg(mock_req: MagicMock, text: str) -> None:
    bot = Bot("token", mock.AsyncMock(), ["mupastir"])
    update_event = get_update_event(text)
    await bot.handle_update(update_event)

    mock_req.assert_not_called()
