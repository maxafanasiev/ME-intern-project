from typing import Annotated

from fastapi import APIRouter, Depends

from app.db.models import User
from app.services.auth_services import auth
from app.services.export_data import ExportDataService
from app.routers.dependencies import export_service

router = APIRouter(tags=['export-data'])


@router.get("/self/json")
async def export_self_user_results_to_json(
        export_service: Annotated[ExportDataService, Depends(export_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await export_service.export_self_user_results_to_json(current_user)


@router.get("/self/csv")
async def export_self_user_results_to_csv(
        export_service: Annotated[ExportDataService, Depends(export_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await export_service.export_self_user_results_to_csv(current_user)


@router.get("/{user_id}/{company_id}/json")
async def export_user_result_in_company_json(
        user_id: int,
        company_id: int,
        export_service: Annotated[ExportDataService, Depends(export_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await export_service.export_user_result_in_company_json(user_id, company_id, current_user)


@router.get("/{user_id}/{company_id}/csv")
async def export_user_result_in_company_csv(
        user_id: int,
        company_id: int,
        export_service: Annotated[ExportDataService, Depends(export_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await export_service.export_user_result_in_company_csv(user_id, company_id, current_user)


@router.get("/company/json/{company_id}")
async def export_all_users_result_in_company_json(
        company_id: int,
        export_service: Annotated[ExportDataService, Depends(export_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await export_service.export_all_users_result_in_company_json(company_id, current_user)


@router.get("/company/csv/{company_id}")
async def export_all_users_result_in_company_csv(
        company_id: int,
        export_service: Annotated[ExportDataService, Depends(export_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await export_service.export_all_users_result_in_company_csv(company_id, current_user)


@router.get("/quiz/json/{quiz_id}")
async def export_users_results_in_quiz_json(
        quiz_id: int,
        export_service: Annotated[ExportDataService, Depends(export_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await export_service.export_users_in_quiz_json(quiz_id, current_user)


@router.get("/quiz/csv/{quiz_id}")
async def export_users_results_in_quiz_csv(
        quiz_id: int,
        export_service: Annotated[ExportDataService, Depends(export_service)],
        current_user: User = Depends(auth.get_current_user)):
    return await export_service.export_users_in_quiz_csv(quiz_id, current_user)
