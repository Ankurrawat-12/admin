"""Audit log endpoints."""
from datetime import datetime
from math import ceil

from fastapi import APIRouter, Query

from app.api.deps import AdminOnly, DbSession
from app.models.audit_log import AuditAction
from app.models.user import User
from app.schemas.audit_log import AuditLogListResponse, AuditLogResponse
from app.services.audit_service import AuditService

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("", response_model=AuditLogListResponse)
async def list_audit_logs(
    db: DbSession,
    current_user: User = AdminOnly,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: int | None = Query(None),
    action: AuditAction | None = Query(None),
    resource_type: str | None = Query(None),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    search: str | None = Query(None),
):
    """List audit logs with pagination and filters (admin only)."""
    audit_service = AuditService(db)
    
    logs, total = await audit_service.get_list(
        page=page,
        page_size=page_size,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        start_date=start_date,
        end_date=end_date,
        search=search,
    )
    
    items = []
    for log in logs:
        item = AuditLogResponse.model_validate(log)
        item.user_email = log.user.email if log.user else None
        items.append(item)
    
    return AuditLogListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=ceil(total / page_size) if total > 0 else 1,
    )
