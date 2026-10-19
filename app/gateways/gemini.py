from typing import Any

from google import genai
from google.genai import errors, types
from langfuse import get_client

from app.models.ai.request import Message

# Gemini names the assistant role "model"; system prompts go to system_instruction instead.
ROLES = {"user": "user", "assistant": "model"}


class GeminiError(Exception):
    pass


def usage_to_langfuse(usage: types.GenerateContentResponseUsageMetadata | None) -> dict[str, int]:
    if usage is None:
        return {}
    # Langfuse usage buckets are exclusive, while Gemini prompt_token_count includes cached tokens.
    cached = usage.cached_content_token_count or 0
    return {
        "input": (usage.prompt_token_count or 0) - cached,
        "input_cached_tokens": cached,
        "output": usage.candidates_token_count or 0,
        "output_reasoning_tokens": usage.thoughts_token_count or 0,
        "total": usage.total_token_count or 0,
    }


class Gemini:
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-3.8-flash",
        timeout: int = 180,
    ):
        self._model = model
        self._client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=timeout * 1000),
        )

    async def complete(
        self,
        messages: list[Message],
        max_tokens: int | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        json: bool | None = None,
        temperature: float | None = None,
        generation_name: str = "generate-content",
    ) -> types.GenerateContentResponse:
        model: str = self._model
        system_instruction = "\n".join(m.content for m in messages if m.role == "system") or None
        contents = [
            types.Content(role=ROLES[m.role], parts=[types.Part(text=m.content)])
            for m in messages
            if m.role != "system"
        ]
        model_parameters: dict[str, Any] = {
            k: v
            for k, v in {
                "max_output_tokens": max_tokens,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty,
                "temperature": temperature,
                "response_mime_type": "application/json" if json else None,
            }.items()
            if v is not None
        }
        config = types.GenerateContentConfig(
            system_instruction=system_instruction, **model_parameters
        )

        with get_client().start_as_current_observation(
            as_type="generation",
            name=generation_name,
            model=model,
            model_parameters=model_parameters,
            input=[m.model_dump() for m in messages],
        ) as generation:
            try:
                response = await self._client.aio.models.generate_content(
                    model=model, contents=contents, config=config
                )
            except errors.APIError as e:
                generation.update(level="ERROR", status_message=str(e))
                raise GeminiError(f"Error: {e.code} - {e.message}") from e
            candidate = response.candidates[0] if response.candidates else None
            generation.update(
                model=response.model_version or model,
                output=response.text,
                usage_details=usage_to_langfuse(response.usage_metadata),
                metadata={
                    "gemini_response_id": response.response_id,
                    "finish_reason": candidate.finish_reason if candidate else None,
                    "block_reason": (
                        response.prompt_feedback.block_reason if response.prompt_feedback else None
                    ),
                },
            )
        return response

    async def easy_complete(
        self, prompt: str, system_prompt: str | None = None, **kwargs: Any
    ) -> str:
        if system_prompt:
            messages = [
                Message(role="system", content=system_prompt),
                Message(role="user", content=prompt),
            ]
        else:
            messages = [Message(role="user", content=prompt)]
        answer = await self.complete(messages, **kwargs)
        if not answer.text:
            raise GeminiError("No response from Gemini")
        return answer.text
