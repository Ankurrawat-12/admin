"""Audit log model for tracking sensitive actions."""
import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AuditAction(str, enum.Enum):
    """Types of auditable actions."""
    # Auth
    login = "login"
    logout = "logout"
    login_failed = "login_failed"
    password_change = "password_change"
    
    # User management
    user_create = "user_create"
    user_update = "user_update"
    user_delete = "user_delete"
    user_role_change = "user_role_change"
    
    # Project management
    project_create = "project_create"
    project_update = "project_update"
    project_delete = "project_delete"
    project_status_change = "project_status_change"


class AuditLog(Base):
    """Audit log for tracking all sensitive actions."""
    
    __tablename__ = "audit_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    action: Mapped[AuditAction] = mapped_column(
        Enum(AuditAction, values_callable=lambda x: [e.value for e in x]), 
        nullable=False, index=True
    )
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    resource_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    
    # Relationships
    user: Mapped["User | None"] = relationship("User", back_populates="audit_logs", lazy="selectin")
    
    def __repr__(self) -> str:
        return f"<AuditLog {self.action} by user {self.user_id}>"


from app.models.user import User
