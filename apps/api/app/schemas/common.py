"""Common schemas used across the application."""
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from app.core.config import settings


T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1)
    page_size: int = Field(
        settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE
    )
    
    @property
    def offset(self) -> int:
        """Calculate offset for database query."""
        return (self.page - 1) * self.page_size


class SortParams(BaseModel):
    """Sorting parameters."""
    sort_by: str = "created_at"
    sort_order: str = Field("desc", pattern="^(asc|desc)$")


class MessageResponse(BaseModel):
    """Simple message response."""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    code: str | None = None
    request_id: str | None = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    environment: str


class StatsResponse(BaseModel):
    """Dashboard statistics response."""
    total_users: int
    total_projects: int
    active_projects: int
    recent_activity_count: int
