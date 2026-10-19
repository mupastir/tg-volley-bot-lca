from datetime import datetime
from json import loads, JSONDecodeError
from typing import Optional, Any, List

from pydantic import BaseModel

from app.models.openai.request import Message


class Choice(BaseModel):
    index: int
    message: Message
    logprobs: Optional[Any]
    finish_reason: Optional[str]

    @property
    def parsed(self) -> Optional[dict]:
        if not self.message:
            return None
        try:
            return loads(self.message.content)
        except JSONDecodeError:
            if self.message.content.startswith("```json"):
                return loads(
                    self.message.content.replace("```json", "").replace("```", "")
                )
            return None


class PromptTokensDetails(BaseModel):
    cached_tokens: int = 0


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    prompt_tokens_details: Optional[PromptTokensDetails] = None

    def to_langfuse(self) -> dict[str, int]:
        # Langfuse usage buckets are exclusive, while OpenAI prompt_tokens includes cached tokens.
        cached = self.prompt_tokens_details.cached_tokens if self.prompt_tokens_details else 0
        return {
            "input": self.prompt_tokens - cached,
            "input_cached_tokens": cached,
            "output": self.completion_tokens,
            "total": self.total_tokens,
        }


class Answer(BaseModel):
    id: str
    object: str
    choices: List[Choice]
    created: datetime
    model: str
    system_fingerprint: Optional[str]
    usage: Usage
