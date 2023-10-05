from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.quiz_schemas import QuizDetailResponse


class CreateQuestionRequestModel(BaseModel):
    question_text: str
    question_answers: List[str]
    question_correct_answers: str


class UpdateQuestionRequestModel(BaseModel):
    question_text: Optional[str]
    question_answers: Optional[List[str]]
    question_correct_answers: Optional[str]


class QuestionDetailResponse(BaseModel):
    id: int
    question_text: str
    question_answers: List[str]
    question_correct_answers: str
    created_at: datetime
    updated_at: datetime
    question_quiz_id: int


class QuestionsListResponse(BaseModel):
    questions: List[QuestionDetailResponse]
