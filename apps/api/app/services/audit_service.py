"""Audit log service for tracking sensitive actions."""
from datetime import datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.audit_log import AuditAction, AuditLog
from app.models.user import User


class AuditService:
    """Service for audit log operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def log(
        self,
        action: AuditAction,
        resource_type: str,
        user_id: int | None = None,
        resource_id: int | None = None,
        details: dict[str, Any] | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
        request_id: str | None = None,
    ) -> AuditLog:
        """Create an audit log entry."""
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            request_id=request_id,
        )
        self.db.add(audit_log)
        await self.db.flush()
        return audit_log
    
    async def get_list(
        self,
        page: int = 1,
        page_size: int = 20,
        user_id: int | None = None,
        action: AuditAction | None = None,
        resource_type: str | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        search: str | None = None,
    ) -> tuple[list[AuditLog], int]:
        """Get paginated list of audit logs with filters."""
        query = select(AuditLog).options(selectinload(AuditLog.user))
        count_query = select(func.count(AuditLog.id))
        
        # Apply filters
        if user_id:
            query = query.where(AuditLog.user_id == user_id)
            count_query = count_query.where(AuditLog.user_id == user_id)
        
        if action:
            query = query.where(AuditLog.action == action)
            count_query = count_query.where(AuditLog.action == action)
        
        if resource_type:
            query = query.where(AuditLog.resource_type == resource_type)
            count_query = count_query.where(AuditLog.resource_type == resource_type)
        
        if start_date:
            query = query.where(AuditLog.created_at >= start_date)
            count_query = count_query.where(AuditLog.created_at >= start_date)
        
        if end_date:
            query = query.where(AuditLog.created_at <= end_date)
            count_query = count_query.where(AuditLog.created_at <= end_date)
        
        if search:
            # Search in request_id or details
            search_filter = f"%{search}%"
            query = query.where(AuditLog.request_id.ilike(search_filter))
            count_query = count_query.where(AuditLog.request_id.ilike(search_filter))
        
        # Order by newest first
        query = query.order_by(AuditLog.created_at.desc())
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # Execute queries
        result = await self.db.execute(query)
        count_result = await self.db.execute(count_query)
        
        return list(result.scalars().all()), count_result.scalar_one()
    
    async def count_recent(self, hours: int = 24) -> int:
        """Get count of audit logs in the last N hours."""
        from datetime import timedelta, timezone
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        result = await self.db.execute(
            select(func.count(AuditLog.id)).where(AuditLog.created_at >= cutoff)
        )
        return result.scalar_one()
