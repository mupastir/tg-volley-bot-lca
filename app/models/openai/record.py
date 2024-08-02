from datetime import datetime

from pydantic import BaseModel


class UserQuestionRecord(BaseModel):
    user_id: int
    question: str
    answer: str
    created_at: datetime
