
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.model import Answer, Question, User
from backend.schemas.answer import CreateAnswer, ResponseAnswer
from backend.security.dependencies import get_current_user


router = APIRouter(tags=["answer"])


@router.post("/question/{ques_id}/answer",response_model=ResponseAnswer,status_code=status.HTTP_201_CREATED)
def create_answer(ques_id: int,answer: CreateAnswer,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):

    # Check whether the question exists
    question = db.get(Question, ques_id)

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    # Create answer using authenticated user's ID
    new_answer = Answer(
        ques_id=ques_id,
        answer=answer.answer,
        user_id=current_user.user_id
    )

    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return ResponseAnswer(
        id=new_answer.ans_id,
        ques_id=new_answer.ques_id,
        answer=new_answer.answer
    )
