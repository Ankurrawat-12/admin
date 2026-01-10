"""User management endpoints."""
from math import ceil

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import AdminOnly, AdminOrManager, CurrentUser, DbSession, RequestInfo
from app.models.audit_log import AuditAction
from app.models.user import User, UserRole
from app.schemas.common import MessageResponse
from app.schemas.user import (
    UserCreate,
    UserListResponse,
    UserPasswordUpdate,
    UserResponse,
    UserUpdate,
)
from app.services.audit_service import AuditService
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=UserListResponse)
async def list_users(
    db: DbSession,
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    search: str | None = Query(None),
    role: UserRole | None = Query(None),
    is_active: bool | None = Query(None),
):
    """List all users with pagination and filters."""
    user_service = UserService(db)
    
    users, total = await user_service.get_list(
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
        search=search,
        role=role,
        is_active=is_active,
    )
    
    return UserListResponse(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
        pages=ceil(total / page_size) if total > 0 else 1,
    )


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    db: DbSession,
    current_user: User = AdminOnly,
    request_info: RequestInfo = None,
):
    """Create a new user (admin only)."""
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    # Check if email already exists
    existing = await user_service.get_by_email(data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user = await user_service.create(data)
    
    # Log user creation
    await audit_service.log(
        action=AuditAction.user_create,
        resource_type="user",
        user_id=current_user.id,
        resource_id=user.id,
        details={"email": user.email, "role": user.role.value},
        **request_info,
    )
    
    return UserResponse.model_validate(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: DbSession,
    current_user: CurrentUser,
):
    """Get user by ID."""
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: DbSession,
    current_user: User = AdminOrManager,
    request_info: RequestInfo = None,
):
    """Update user (admin/manager only)."""
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Only admins can change roles
    if data.role is not None and current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can change user roles",
        )
    
    # Track role changes for audit
    old_role = user.role
    
    # Check email uniqueness if changing
    if data.email and data.email != user.email:
        existing = await user_service.get_by_email(data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
    
    updated_user = await user_service.update(user, data)
    
    # Log role change specifically
    if data.role and data.role != old_role:
        await audit_service.log(
            action=AuditAction.user_role_change,
            resource_type="user",
            user_id=current_user.id,
            resource_id=user_id,
            details={"old_role": old_role.value, "new_role": data.role.value},
            **request_info,
        )
    else:
        await audit_service.log(
            action=AuditAction.user_update,
            resource_type="user",
            user_id=current_user.id,
            resource_id=user_id,
            details=data.model_dump(exclude_unset=True),
            **request_info,
        )
    
    return UserResponse.model_validate(updated_user)


@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(
    user_id: int,
    db: DbSession,
    current_user: User = AdminOnly,
    request_info: RequestInfo = None,
):
    """Delete user (admin only)."""
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Prevent self-deletion
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )
    
    # Log before deletion
    await audit_service.log(
        action=AuditAction.user_delete,
        resource_type="user",
        user_id=current_user.id,
        resource_id=user_id,
        details={"email": user.email},
        **request_info,
    )
    
    await user_service.delete(user)
    
    return MessageResponse(message="User deleted successfully")


@router.post("/me/password", response_model=MessageResponse)
async def change_password(
    data: UserPasswordUpdate,
    db: DbSession,
    current_user: CurrentUser,
    request_info: RequestInfo,
):
    """Change current user's password."""
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    # Verify current password
    from app.core.security import verify_password
    if not verify_password(data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    
    await user_service.update_password(current_user, data.new_password)
    
    await audit_service.log(
        action=AuditAction.password_change,
        resource_type="user",
        user_id=current_user.id,
        resource_id=current_user.id,
        **request_info,
    )
    
    return MessageResponse(message="Password updated successfully")
