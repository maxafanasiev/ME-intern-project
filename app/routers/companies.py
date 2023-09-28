from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.db.models import User
from app.routers.dependencies import company_service
from app.schemas.validation_schemas import PaginationQueryParams
from app.services.auth_services import auth
from app.services.companies import CompanyService
from app.schemas.company_schemas import CompanyListResponse, CompanyDetailResponse, CompanyUpdateRequestModel, \
    CreateCompanyRequestModel

router = APIRouter(tags=["companies"])


@router.post("/", response_model=CompanyDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_company(body: CreateCompanyRequestModel,
                         company_service: Annotated[CompanyService, Depends(company_service)],
                         current_user: User = Depends(auth.get_current_user)):
    return await company_service.create_company(body, current_user)


@router.get("/{company_id}", response_model=CompanyDetailResponse)
async def get_company_by_id(company_id: int, company_service: Annotated[CompanyService, Depends(company_service)]):
    return await company_service.get_company_by_id(company_id)


@router.put("/{company_id}", response_model=CompanyDetailResponse)
async def update_company(body: CompanyUpdateRequestModel,
                         company_service: Annotated[CompanyService, Depends(company_service)],
                         company_id: int,
                         current_user: User = Depends(auth.get_current_user)):
    return await company_service.update_company(company_id, body, current_user)


@router.delete("/{company_id}", response_model=CompanyDetailResponse)
async def delete_company(company_service: Annotated[CompanyService, Depends(company_service)],
                         company_id: int,
                         current_user: User = Depends(auth.get_current_user)):
    return await company_service.delete_company(company_id, current_user)


@router.get("/", response_model=CompanyListResponse)
async def get_companies(company_service: Annotated[CompanyService, Depends(company_service)],
                        params: PaginationQueryParams = Depends()):
    return await company_service.get_all_companies(params.page, params.size)
