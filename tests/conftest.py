import pytest
from minigram import MiniGramUpdate


@pytest.fixture
def minigram_update_start_message():
    return MiniGramUpdate(
        data={
            "update_id": 1,
            "message": {
                "message_id": 1,
                "date": 1,
                "text": "/start",
                "chat": {
                    "id": 1,
                    "type": "private",
                },
            },
        }
    )


@pytest.fixture
def minigram_update_help_message():
    return MiniGramUpdate(
        data={
            "update_id": 1,
            "message": {
                "message_id": 2,
                "date": 1,
                "text": "/help",
                "chat": {
                    "id": 1,
                    "type": "private",
                },
            },
        }
    )


@pytest.fixture
def minigram_update_wrong_command():
    return MiniGramUpdate(
        data={
            "update_id": 1,
            "message": {
                "message_id": 3,
                "date": 1,
                "text": "/abracadabra",
                "chat": {
                    "id": 1,
                    "type": "private",
                },
            },
        }
    )


@pytest.fixture
def minigram_update_about_message():
    return MiniGramUpdate(
        data={
            "update_id": 1,
            "message": {
                "message_id": 4,
                "date": 1,
                "text": "fact!",
                "chat": {
                    "id": 1,
                    "type": "private",
                },
            },
        }
    )
