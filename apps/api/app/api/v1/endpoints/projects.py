"""Project management endpoints."""
from math import ceil

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import AdminOrManager, CurrentUser, DbSession, RequestInfo
from app.models.audit_log import AuditAction
from app.models.project import ProjectStatus
from app.models.user import User, UserRole
from app.schemas.common import MessageResponse
from app.schemas.project import (
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.audit_service import AuditService
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    db: DbSession,
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    search: str | None = Query(None),
    status: ProjectStatus | None = Query(None),
    owner_id: int | None = Query(None),
):
    """List all projects with pagination and filters."""
    project_service = ProjectService(db)
    
    projects, total = await project_service.get_list(
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
        search=search,
        status=status,
        owner_id=owner_id,
    )
    
    return ProjectListResponse(
        items=[ProjectResponse.model_validate(p) for p in projects],
        total=total,
        page=page,
        page_size=page_size,
        pages=ceil(total / page_size) if total > 0 else 1,
    )


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    data: ProjectCreate,
    db: DbSession,
    current_user: User = AdminOrManager,
    request_info: RequestInfo = None,
):
    """Create a new project (admin/manager only)."""
    project_service = ProjectService(db)
    audit_service = AuditService(db)
    
    project = await project_service.create(data, current_user.id)
    
    # Reload to get owner relationship
    project = await project_service.get_by_id(project.id)
    
    await audit_service.log(
        action=AuditAction.project_create,
        resource_type="project",
        user_id=current_user.id,
        resource_id=project.id,
        details={"name": project.name, "status": project.status.value},
        **request_info,
    )
    
    return ProjectResponse.model_validate(project)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    """Get project by ID."""
    project_service = ProjectService(db)
    project = await project_service.get_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    return ProjectResponse.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: DbSession,
    current_user: User = AdminOrManager,
    request_info: RequestInfo = None,
):
    """Update project (admin/manager only)."""
    project_service = ProjectService(db)
    audit_service = AuditService(db)
    
    project = await project_service.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Managers can only edit their own projects
    if current_user.role == UserRole.manager and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Managers can only edit their own projects",
        )
    
    old_status = project.status
    updated_project = await project_service.update(project, data)
    
    # Log status change specifically
    if data.status and data.status != old_status:
        await audit_service.log(
            action=AuditAction.project_status_change,
            resource_type="project",
            user_id=current_user.id,
            resource_id=project_id,
            details={"old_status": old_status.value, "new_status": data.status.value},
            **request_info,
        )
    else:
        await audit_service.log(
            action=AuditAction.project_update,
            resource_type="project",
            user_id=current_user.id,
            resource_id=project_id,
            details=data.model_dump(exclude_unset=True),
            **request_info,
        )
    
    return ProjectResponse.model_validate(updated_project)


@router.delete("/{project_id}", response_model=MessageResponse)
async def delete_project(
    project_id: int,
    db: DbSession,
    current_user: User = AdminOrManager,
    request_info: RequestInfo = None,
):
    """Delete project (admin/manager only, managers only their own)."""
    project_service = ProjectService(db)
    audit_service = AuditService(db)
    
    project = await project_service.get_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    
    # Managers can only delete their own projects
    if current_user.role == UserRole.manager and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Managers can only delete their own projects",
        )
    
    await audit_service.log(
        action=AuditAction.project_delete,
        resource_type="project",
        user_id=current_user.id,
        resource_id=project_id,
        details={"name": project.name},
        **request_info,
    )
    
    await project_service.delete(project)
    
    return MessageResponse(message="Project deleted successfully")
