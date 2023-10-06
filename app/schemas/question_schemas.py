from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator


class Question(BaseModel):
    id: int
    question_text: str
    question_answers: List[str]
    question_quiz_id: int


class CreateQuestionRequestModel(BaseModel):
    question_text: str
    question_answers: List[str]
    question_correct_answers: str

    @field_validator("question_answers")
    def prevent_email_change(cls, value):
        if len(value) < 2:
            raise ValueError("Question must have at least 2 answers")
        return value


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
    questions: List[Question]
