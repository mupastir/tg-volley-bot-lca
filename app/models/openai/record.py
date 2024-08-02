from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, Field, AfterValidator, PlainSerializer, UUID4


def to_str(value: Any) -> str:
    return str(value)


Uuid4Str = Annotated[
    UUID4,
    Field(validate_default=True),
    AfterValidator(to_str),
    PlainSerializer(lambda x: x, return_type=str),
]


class UserQuestionRecord(BaseModel):
    id: Uuid4Str
    user_id: int
    question: str
    answer: str
    created_at: datetime
    expires_at: int
