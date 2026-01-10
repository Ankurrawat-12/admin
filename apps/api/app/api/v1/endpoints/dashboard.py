"""Dashboard endpoints for KPIs and stats."""
from fastapi import APIRouter

from app.api.deps import CurrentUser, DbSession
from app.schemas.common import StatsResponse
from app.services.audit_service import AuditService
from app.services.project_service import ProjectService
from app.services.user_service import UserService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=StatsResponse)
async def get_dashboard_stats(
    db: DbSession,
    current_user: CurrentUser,
):
    """Get dashboard statistics."""
    user_service = UserService(db)
    project_service = ProjectService(db)
    audit_service = AuditService(db)
    
    total_users = await user_service.count()
    total_projects = await project_service.count()
    active_projects = await project_service.count_active()
    recent_activity = await audit_service.count_recent(hours=24)
    
    return StatsResponse(
        total_users=total_users,
        total_projects=total_projects,
        active_projects=active_projects,
        recent_activity_count=recent_activity,
    )
