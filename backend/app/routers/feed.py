# backend/app/routers/feed.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.model import Question, Answer
from backend.schemas.feed import FeedItem, FeedResponse

router = APIRouter(tags=["feed"])


@router.get("/feed", response_model=FeedResponse)
def get_feed(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):

    PAGE_SIZE = 10

    # Fetch 11 questions to check whether another page exists
    questions = (
        db.query(Question)
        .order_by(Question.created_at.desc(), Question.ques_id.desc())
        .offset((page - 1) * PAGE_SIZE)
        .limit(PAGE_SIZE + 1)
        .all()
    )

    has_next = len(questions) > PAGE_SIZE

    questions = questions[:PAGE_SIZE]

    feed_items = []

    for question in questions:

        # Find the latest answer for this question
        latest_answer = (
            db.query(Answer)
            .filter(Answer.ques_id == question.ques_id)
            .order_by(Answer.created_at.desc(), Answer.ans_id.desc())
            .first()
        )

        feed_items.append(
            FeedItem(
                ques_id=question.ques_id,
                question=question.question,
                question_created_at=question.created_at,

                ans_id=latest_answer.ans_id if latest_answer else None,
                answer=latest_answer.answer if latest_answer else None,
                answer_created_at=latest_answer.created_at if latest_answer else None
            )
        )

    return FeedResponse(
        page=page,
        page_size=PAGE_SIZE,
        has_next=has_next,
        items=feed_items
    )