"""Audit log schemas for request/response validation."""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.audit_log import AuditAction


# Response schemas
class AuditLogResponse(BaseModel):
    """Audit log response schema."""
    id: int
    user_id: int | None
    action: AuditAction
    resource_type: str
    resource_id: int | None
    details: dict[str, Any] | None
    ip_address: str | None
    user_agent: str | None
    request_id: str | None
    created_at: datetime
    user_email: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


class AuditLogListResponse(BaseModel):
    """Paginated audit log list response."""
    items: list[AuditLogResponse]
    total: int
    page: int
    page_size: int
    pages: int


# Filter schemas
class AuditLogFilter(BaseModel):
    """Filter options for audit logs."""
    user_id: int | None = None
    action: AuditAction | None = None
    resource_type: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    search: str | None = None
