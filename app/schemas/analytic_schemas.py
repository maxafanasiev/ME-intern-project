from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class UserGlobalAnalytics(BaseModel):
    user_id: int
    rating: float


class QuizAnalytics(BaseModel):
    quiz_id: int
    completion_time: datetime
    average_score: float


class UserQuizzesScoreAnalytics(BaseModel):
    results: List[QuizAnalytics]


class QuizLastAttemptAnalytics(BaseModel):
    quiz_id: int
    quiz_name: str
    last_attempt_time: datetime


class ListQuizLastAttemptAnalytics(BaseModel):
    quizzes: List[QuizLastAttemptAnalytics]


class UserResultAnalytics(BaseModel):
    user_id: int
    user_firstname: str
    user_lastname: str
    quiz_id: int
    quiz_name: str
    score: float
    completion_time: datetime


class ListUserResultAnalytics(BaseModel):
    users_results: List[UserResultAnalytics]


class QuizResultAnalytics(BaseModel):
    user_id: int
    quiz_id: int
    quiz_name: str
    score: float
    completion_time: datetime


class ListQuizResultAnalytics(BaseModel):
    quizzes_result: List[QuizResultAnalytics]


class UserLastCompletionTimeAnalytics(BaseModel):
    user_id: int
    user_firstname: str
    user_lastname: str
    last_completion_time: datetime


class ListUserLastCompletionTimeAnalytics(BaseModel):
    users_last_completion_time: List[UserLastCompletionTimeAnalytics]
