from datetime import datetime

import pytest

from app import MiniGramUpdate
from random import choice as randchoice

from app.handlers.actions.ask_ai_handler import OPENAI_MODIFIERS
from app.models.openai.request import Message
from app.models.openai.response import Answer, Choice, Usage


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
                "user": {
                    "id": 1,
                    "username": "testuser",
                    "is_bot": False,
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
                "user": {
                    "id": 1,
                    "username": "testuser",
                    "is_bot": False,
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
                "user": {
                    "id": 1,
                },
                "from": {
                    "id": 1,
                    "username": "testuser",
                    "is_bot": False,
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
                "text": randchoice(["fact!", "oneliner!"]),
                "chat": {
                    "id": 1,
                    "type": "private",
                },
                "user": {
                    "id": 1,
                },
                "from": {
                    "id": 1,
                    "username": "testuser",
                    "is_bot": False,
                },
            },
        }
    )


@pytest.fixture
def minigram_update_ask_openai_message():
    return MiniGramUpdate(
        data={
            "update_id": 1,
            "message": {
                "message_id": 5,
                "date": 1,
                "text": f"{randchoice(OPENAI_MODIFIERS)} How to serve skyball?",
                "chat": {
                    "id": 1,
                    "type": "private",
                },
                "user": {
                    "id": 1,
                },
                "from": {
                    "id": 1,
                    "username": "testuser",
                    "is_bot": False,
                },
            },
        }
    )


@pytest.fixture
def minigram_update_ask_openai_short_message():
    short_messages = ["How?", "idle"]
    return MiniGramUpdate(
        data={
            "update_id": 1,
            "message": {
                "message_id": 5,
                "date": 1,
                "text": f"{randchoice(OPENAI_MODIFIERS)} {randchoice(short_messages)}",
                "chat": {
                    "id": 1,
                    "type": "private",
                },
                "user": {
                    "id": 1,
                },
                "from": {
                    "id": 1,
                    "username": "testuser",
                    "is_bot": False,
                },
            },
        }
    )


@pytest.fixture
def openai_response():
    return Answer(
        id="1",
        object="",
        choices=[
            Choice(
                index=0,
                message=Message(role="assistant", content="Answer from OpenAI"),
                logprobs=None,
                finish_reason=None,
            )
        ],
        created=datetime.now(),
        model="",
        system_fingerprint=None,
        usage=Usage(prompt_tokens=0, completion_tokens=0, total_tokens=0),
    )
