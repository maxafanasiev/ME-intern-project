from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.db.models import User
from app.routers.dependencies import question_service
from app.services.auth_services import auth
from app.services.questions import QuestionService
from app.schemas.question_schemas import QuestionDetailResponse, QuestionsListResponse, CreateQuestionRequestModel, \
    UpdateQuestionRequestModel

router = APIRouter(tags=["questions"])


@router.post("/add-question-to-quiz/{quiz_id}",
             response_model=QuestionDetailResponse,
             status_code=status.HTTP_201_CREATED)
async def create_question(body: CreateQuestionRequestModel,
                          quiz_id: int,
                          question_service: Annotated[QuestionService, Depends(question_service)],
                          current_user: User = Depends(auth.get_current_user)):
    return await question_service.create_question(body, quiz_id, current_user)


@router.get("/{question_id}", response_model=QuestionDetailResponse)
async def get_question_by_id(question_id: int, question_service: Annotated[QuestionService, Depends(question_service)]):
    return await question_service.get_question_by_id(question_id)


@router.put("/{question_id}", response_model=QuestionDetailResponse)
async def update_question(body: UpdateQuestionRequestModel,
                          question_service: Annotated[QuestionService, Depends(question_service)],
                          question_id: int,
                          current_user: User = Depends(auth.get_current_user)):
    return await question_service.update_question(question_id, body, current_user)


@router.delete("/{question_id}", response_model=QuestionDetailResponse)
async def delete_question(question_service: Annotated[QuestionService, Depends(question_service)],
                          question_id: int,
                          current_user: User = Depends(auth.get_current_user)):
    return await question_service.delete_question(question_id, current_user)


@router.get("/all-in-quiz/{quiz_id}", response_model=QuestionsListResponse)
async def get_question_in_quiz(quiz_id: int,
                               question_service: Annotated[QuestionService, Depends(question_service)]):
    return await question_service.get_all_question_in_quiz(quiz_id)
