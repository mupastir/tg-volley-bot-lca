# Shortcut imports with temporary mock find_spec until usage with aiohttp won't be fixed in MiniGram library.
from unittest import mock


def find_spec(name: str) -> str | None:
    if name in ("aiohttp", "starlette"):
        return None
    return name


with mock.patch("importlib.util.find_spec") as mock_find_spec:
    mock_find_spec.side_effect = find_spec
    from minigram import AsyncMiniGram, MiniGramUpdate


__all__ = ["AsyncMiniGram", "MiniGramUpdate"]
