"""Project schemas for request/response validation."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.project import ProjectPriority, ProjectStatus
from app.schemas.user import UserResponse


# Base schemas
class ProjectBase(BaseModel):
    """Base project schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    status: ProjectStatus = ProjectStatus.draft
    priority: ProjectPriority = ProjectPriority.medium
    budget: int | None = Field(None, ge=0)  # In cents
    start_date: datetime | None = None
    end_date: datetime | None = None


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    owner_id: int | None = None  # If not provided, uses current user


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: ProjectStatus | None = None
    priority: ProjectPriority | None = None
    budget: int | None = Field(None, ge=0)
    start_date: datetime | None = None
    end_date: datetime | None = None
    owner_id: int | None = None


# Response schemas
class ProjectResponse(ProjectBase):
    """Project response schema."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    owner: UserResponse | None = None
    
    model_config = ConfigDict(from_attributes=True)


class ProjectListResponse(BaseModel):
    """Paginated project list response."""
    items: list[ProjectResponse]
    total: int
    page: int
    page_size: int
    pages: int
