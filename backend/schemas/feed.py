# regret/backend/schemas/feed.py

from pydantic import BaseModel
from datetime import datetime


class FeedItem(BaseModel):
    ques_id: int
    question: str
    question_created_at: datetime

    ans_id: int | None = None
    answer: str | None = None
    answer_created_at: datetime | None = None


class FeedResponse(BaseModel):
    page: int
    page_size: int
    has_next: bool
    items: list[FeedItem]
