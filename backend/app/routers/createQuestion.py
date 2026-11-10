# backend/app/routers/createQuestion.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.database.model import Question,User
from backend.schemas.question import CreateQuestion, ResponseQuestion
from backend.security.dependencies import get_current_user

router = APIRouter(tags=["question"])


@router.post("/question",response_model=ResponseQuestion,status_code=status.HTTP_201_CREATED)
def create_question(question: CreateQuestion,db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    
    new_question = Question(
        question=question.question,
        user_id=current_user.user_id
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return ResponseQuestion(
        id=new_question.ques_id,
        question=new_question.question
    )