from datetime import datetime

from pydantic import BaseModel


class QuizResultResponse(BaseModel):
    result_user_id: int
    result_company_id: int
    result_quiz_id: int
    result_right_count: int
    result_total_count: int
    created_at: datetime


class Answer(BaseModel):
    question_id: int
    answer: str


class RatingInCompany(BaseModel):
    user_id: int
    company_id: int
    average_score: float


class RatingGlobal(BaseModel):
    user_id: int
    average_score: float
