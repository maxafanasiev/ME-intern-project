from typing import Annotated

from fastapi import APIRouter, Depends

from app.routers.dependencies import score_service
from app.schemas.quiz_workflow_schemas import RatingInCompany, RatingGlobal
from app.services.scores import ScoreService

router = APIRouter(tags=["scores"])


@router.get("/{user_id}/{company_id}", response_model=RatingInCompany)
async def get_user_score_in_company(user_id: int,
                                    company_id: int,
                                    score_service: Annotated[ScoreService, Depends(score_service)]):
    return await score_service.get_user_score_in_company(user_id, company_id)


@router.get("/{user_id}", response_model=RatingGlobal)
async def get_user_score_in_company(user_id: int,
                                    score_service: Annotated[ScoreService, Depends(score_service)]):
    return await score_service.get_user_score_global(user_id)

