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


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Answer(BaseModel):
    id: str
    object: str
    choices: List[Choice]
    created: datetime
    model: str
    system_fingerprint: Optional[str]
    usage: Usage
