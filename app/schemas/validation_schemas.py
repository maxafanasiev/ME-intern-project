from pydantic import BaseModel, Field


class PaginationQueryParams(BaseModel):
    page: int = Field(default=1, description="Page number, starting from 1", ge=1)
    size: int = Field(default=10, description="Number of items per page", le=1000)