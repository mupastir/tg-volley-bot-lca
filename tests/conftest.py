from datetime import datetime

import pytest

from random import choice as randchoice

from app.handlers.actions.ask_ai_handler import OPENAI_MODIFIERS
from app.models.openai.request import Message
from app.models.openai.response import Answer, Choice, Usage
from tests.helpers import get_update_event


@pytest.fixture
def minigram_update_start_message():
    return get_update_event("/start")


@pytest.fixture
def minigram_update_help_message():
    return get_update_event("/help")


@pytest.fixture
def minigram_update_wrong_command():
    return get_update_event("/abracadabra")


@pytest.fixture
def minigram_update_about_message():
    return get_update_event(randchoice(["fact!", "oneliner!"]))


@pytest.fixture
def minigram_update_ask_openai_message():
    return get_update_event(f"{randchoice(OPENAI_MODIFIERS)} How to serve skyball?")


@pytest.fixture
def minigram_update_ask_openai_short_message():
    short_messages = ["How?", "idle"]
    return get_update_event(
        f"{randchoice(OPENAI_MODIFIERS)} {randchoice(short_messages)}"
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
