"""User service for business logic."""
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service for user operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_by_id(self, user_id: int) -> User | None:
        """Get user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_list(
        self,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        search: str | None = None,
        role: UserRole | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[User], int]:
        """Get paginated list of users with filters."""
        query = select(User)
        count_query = select(func.count(User.id))
        
        # Apply filters
        if search:
            search_filter = f"%{search}%"
            query = query.where(
                (User.email.ilike(search_filter)) | (User.full_name.ilike(search_filter))
            )
            count_query = count_query.where(
                (User.email.ilike(search_filter)) | (User.full_name.ilike(search_filter))
            )
        
        if role:
            query = query.where(User.role == role)
            count_query = count_query.where(User.role == role)
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
            count_query = count_query.where(User.is_active == is_active)
        
        # Apply sorting
        sort_column = getattr(User, sort_by, User.created_at)
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
    
    async def create(self, data: UserCreate) -> User:
        """Create a new user."""
        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=get_password_hash(data.password),
            role=data.role,
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def update(self, user: User, data: UserUpdate) -> User:
        """Update a user."""
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def update_password(self, user: User, new_password: str) -> User:
        """Update user password."""
        user.hashed_password = get_password_hash(new_password)
        await self.db.flush()
        await self.db.refresh(user)
        return user
    
    async def update_last_login(self, user: User) -> User:
        """Update last login timestamp."""
        user.last_login = datetime.now(timezone.utc)
        await self.db.flush()
        return user
    
    async def delete(self, user: User) -> None:
        """Delete a user."""
        await self.db.delete(user)
        await self.db.flush()
    
    async def authenticate(self, email: str, password: str) -> User | None:
        """Authenticate user by email and password."""
        user = await self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user
    
    async def count(self) -> int:
        """Get total user count."""
        result = await self.db.execute(select(func.count(User.id)))
        return result.scalar_one()
