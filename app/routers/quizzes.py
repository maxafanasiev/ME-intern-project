from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.db.models import User
from app.routers.dependencies import quiz_service
from app.schemas.pagination_schemas import PaginationQueryParams
from app.schemas.question_schemas import QuestionsListResponse
from app.schemas.quiz_workflow_schemas import QuizResultResponse
from app.services.auth_services import auth
from app.services.quizzes import QuizService
from app.schemas.quiz_schemas import QuizDetailResponse, QuizUpdateRequestModel, CreateQuizRequestModel, \
    QuizListResponse, QuizStartRequest

router = APIRouter(tags=["quizzes"])


@router.post("/{company_id}", response_model=QuizDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz(body: CreateQuizRequestModel,
                      company_id: int,
                      quiz_service: Annotated[QuizService, Depends(quiz_service)],
                      current_user: User = Depends(auth.get_current_user)):
    return await quiz_service.create_quiz(body, company_id, current_user)


@router.get("/quiz/{quiz_id}", response_model=QuizDetailResponse)
async def get_quiz_by_id(quiz_id: int, quiz_service: Annotated[QuizService, Depends(quiz_service)]):
    return await quiz_service.get_quiz_by_id(quiz_id)


@router.put("/{quiz_id}", response_model=QuizDetailResponse)
async def update_quiz(body: QuizUpdateRequestModel,
                      quiz_service: Annotated[QuizService, Depends(quiz_service)],
                      quiz_id: int,
                      current_user: User = Depends(auth.get_current_user)):
    return await quiz_service.update_quiz(quiz_id, body, current_user)


@router.delete("/{quiz_id}", response_model=QuizDetailResponse)
async def delete_quiz(quiz_service: Annotated[QuizService, Depends(quiz_service)],
                      quiz_id: int,
                      current_user: User = Depends(auth.get_current_user)):
    return await quiz_service.delete_quiz(quiz_id, current_user)


@router.get("/{company_id}", response_model=QuizListResponse)
async def get_quizzes_in_company(company_id: int,
                                 quiz_service: Annotated[QuizService, Depends(quiz_service)],
                                 params: PaginationQueryParams = Depends()):
    return await quiz_service.get_all_quizzes_in_company(company_id, params.page, params.size)


@router.post("/start/{quiz_id}", response_model=QuestionsListResponse)
async def start_quiz(quiz_id: int,
                     quiz_service: Annotated[QuizService, Depends(quiz_service)],
                     current_user: User = Depends(auth.get_current_user)):
    return await quiz_service.start_quiz(quiz_id, current_user)


@router.post("/submit/{quiz_id}", response_model=QuizResultResponse)
async def finish_quiz(body: QuizStartRequest,
                      quiz_id: int,
                      quiz_service: Annotated[QuizService, Depends(quiz_service)],
                      current_user: User = Depends(auth.get_current_user)):
    return await quiz_service.get_quiz_result(quiz_id, body, current_user)
