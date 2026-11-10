# regret/backend/schemas/question.py

from pydantic import BaseModel


class CreateQuestion(BaseModel):
    question: str


class ResponseQuestion(BaseModel):
    id: int
    question: str