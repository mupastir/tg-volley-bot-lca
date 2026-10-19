from unittest import mock

from google.genai import types

from app.gateways.gemini import Gemini, usage_to_langfuse
from app.models.ai.request import Message


async def test_complete_maps_messages_to_gemini_request(
    gemini_response: types.GenerateContentResponse,
) -> None:
    gemini = Gemini("key", model="gemini-test")
    generate = mock.AsyncMock(return_value=gemini_response)
    with mock.patch.object(gemini._client.aio.models, "generate_content", generate):
        answer = await gemini.complete(
            [
                Message(role="system", content="Be funny."),
                Message(role="user", content="Hi"),
                Message(role="assistant", content="Hello"),
                Message(role="user", content="How to serve skyball?"),
            ],
            max_tokens=100,
            temperature=1.1,
        )

    assert answer.text == "Answer from AI"
    kwargs = generate.call_args.kwargs
    assert kwargs["model"] == "gemini-test"
    assert [(c.role, c.parts[0].text) for c in kwargs["contents"]] == [
        ("user", "Hi"),
        ("model", "Hello"),
        ("user", "How to serve skyball?"),
    ]
    config = kwargs["config"]
    assert config.system_instruction == "Be funny."
    assert config.max_output_tokens == 100
    assert config.temperature == 1.1


def test_usage_to_langfuse_splits_cached_tokens() -> None:
    usage = types.GenerateContentResponseUsageMetadata(
        prompt_token_count=100,
        cached_content_token_count=40,
        candidates_token_count=20,
        thoughts_token_count=5,
        total_token_count=125,
    )
    assert usage_to_langfuse(usage) == {
        "input": 60,
        "input_cached_tokens": 40,
        "output": 20,
        "output_reasoning_tokens": 5,
        "total": 125,
    }
