from random import choice as randchoice

import pytest
from google.genai import types

from app.handlers.actions.ask_ai_handler import AI_MODIFIERS
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
def minigram_update_ask_ai_message():
    return get_update_event(f"{randchoice(AI_MODIFIERS)} How to serve skyball?")


@pytest.fixture
def minigram_update_ask_ai_short_message():
    short_messages = ["How?", "idle"]
    return get_update_event(
        f"{randchoice(AI_MODIFIERS)} {randchoice(short_messages)}"
    )


@pytest.fixture
def gemini_response():
    return types.GenerateContentResponse(
        candidates=[
            types.Candidate(
                content=types.Content(role="model", parts=[types.Part(text="Answer from AI")]),
                finish_reason=types.FinishReason.STOP,
            )
        ],
        model_version="gemini-3.8-flash",
        usage_metadata=types.GenerateContentResponseUsageMetadata(
            prompt_token_count=0, candidates_token_count=0, total_token_count=0
        ),
    )
