# backend/schemas/answer.py

from pydantic import BaseModel


class CreateAnswer(BaseModel):
    answer: str


class ResponseAnswer(BaseModel):
    id: int
    ques_id: int
    answer: str