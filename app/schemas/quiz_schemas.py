from datetime import datetime
from typing import Optional, List, Dict

from pydantic import BaseModel, Field

from app.db.models import Company
from app.schemas.company_schemas import CompanyDetailResponse
from app.schemas.quiz_workflow_schemas import Answer


class CreateQuizRequestModel(BaseModel):
    quiz_name: str
    quiz_title: Optional[str]
    quiz_description: Optional[str]
    quiz_frequency: Optional[int]


class QuizUpdateRequestModel(BaseModel):
    quiz_name: Optional[str] = Field(min_length=1, max_length=255, default=None)
    quiz_title: Optional[str] = Field(min_length=1, max_length=100, default=None)
    quiz_description: Optional[str] = Field(min_length=1, default=None)
    quiz_frequency: Optional[int] = Field(default=0)


class QuizDetailResponse(BaseModel):
    id: int
    quiz_name: str
    quiz_title: Optional[str]
    quiz_description: Optional[str]
    quiz_frequency: int
    created_at: datetime
    updated_at: datetime
    quiz_company_id: int


class QuizListResponse(BaseModel):
    quizzes: List[QuizDetailResponse]


class QuizStartRequest(BaseModel):
    answers: List[Answer]



