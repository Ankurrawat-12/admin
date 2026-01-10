"""Project service for business logic."""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import Project, ProjectStatus
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """Service for project operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, project_id: int, include_owner: bool = True) -> Project | None:
        """Get project by ID."""
        query = select(Project).where(Project.id == project_id)
        if include_owner:
            query = query.options(selectinload(Project.owner))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_list(
        self,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        search: str | None = None,
        status: ProjectStatus | None = None,
        owner_id: int | None = None,
    ) -> tuple[list[Project], int]:
        """Get paginated list of projects with filters."""
        query = select(Project).options(selectinload(Project.owner))
        count_query = select(func.count(Project.id))
        
        # Apply filters
        if search:
            search_filter = f"%{search}%"
            query = query.where(
                (Project.name.ilike(search_filter)) | 
                (Project.description.ilike(search_filter))
            )
            count_query = count_query.where(
                (Project.name.ilike(search_filter)) | 
                (Project.description.ilike(search_filter))
            )
        
        if status:
            query = query.where(Project.status == status)
            count_query = count_query.where(Project.status == status)
        
        if owner_id:
            query = query.where(Project.owner_id == owner_id)
            count_query = count_query.where(Project.owner_id == owner_id)
        
        # Apply sorting
        sort_column = getattr(Project, sort_by, Project.created_at)
        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Apply pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        
        # Execute queries
        result = await self.db.execute(query)
        count_result = await self.db.execute(count_query)
        
        return list(result.scalars().all()), count_result.scalar_one()
    
    async def create(self, data: ProjectCreate, owner_id: int) -> Project:
        """Create a new project."""
        project = Project(
            name=data.name,
            description=data.description,
            status=data.status,
            priority=data.priority,
            budget=data.budget,
            start_date=data.start_date,
            end_date=data.end_date,
            owner_id=data.owner_id or owner_id,
        )
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project
    
    async def update(self, project: Project, data: ProjectUpdate) -> Project:
        """Update a project."""
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        await self.db.flush()
        await self.db.refresh(project)
        return project
    
    async def delete(self, project: Project) -> None:
        """Delete a project."""
        await self.db.delete(project)
        await self.db.flush()
    
    async def count(self, status: ProjectStatus | None = None) -> int:
        """Get project count, optionally filtered by status."""
        query = select(func.count(Project.id))
        if status:
            query = query.where(Project.status == status)
        result = await self.db.execute(query)
        return result.scalar_one()
    
    async def count_active(self) -> int:
        """Get count of active projects."""
        return await self.count(status=ProjectStatus.active)
