"""Project model."""
import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProjectStatus(str, enum.Enum):
    """Project status options."""
    draft = "draft"
    active = "active"
    on_hold = "on_hold"
    completed = "completed"
    archived = "archived"


class ProjectPriority(str, enum.Enum):
    """Project priority levels."""
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Project(Base):
    """Project model for managing projects."""
    
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, values_callable=lambda x: [e.value for e in x]), 
        default=ProjectStatus.draft, nullable=False
    )
    priority: Mapped[ProjectPriority] = mapped_column(
        Enum(ProjectPriority, values_callable=lambda x: [e.value for e in x]), 
        default=ProjectPriority.medium, nullable=False
    )
    budget: Mapped[int | None] = mapped_column(Integer, nullable=True)  # In cents
    start_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    
    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="projects", lazy="selectin")
    
    def __repr__(self) -> str:
        return f"<Project {self.name}>"


from app.models.user import User
