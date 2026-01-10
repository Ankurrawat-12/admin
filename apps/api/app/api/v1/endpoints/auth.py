"""Authentication endpoints."""
from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentUser, DbSession, RequestInfo
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.models.audit_log import AuditAction
from app.schemas.auth import AuthResponse, LoginRequest, RefreshTokenRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.audit_service import AuditService
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=AuthResponse)
async def login(
    data: LoginRequest,
    db: DbSession,
    request_info: RequestInfo,
):
    """Authenticate user and return tokens."""
    user_service = UserService(db)
    audit_service = AuditService(db)
    
    user = await user_service.authenticate(data.email, data.password)
    
    if not user:
        # Log failed login attempt
        await audit_service.log(
            action=AuditAction.login_failed,
            resource_type="auth",
            details={"email": data.email},
            **request_info,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Update last login
    await user_service.update_last_login(user)
    
    # Log successful login
    await audit_service.log(
        action=AuditAction.login,
        resource_type="auth",
        user_id=user.id,
        **request_info,
    )
    
    # Refresh user to get updated fields (last_login, updated_at)
    await db.refresh(user)
    
    # Create tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        ),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest, db: DbSession):
    """Refresh access token using refresh token."""
    payload = decode_token(data.refresh_token)
    
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    # Verify user still exists and is active
    user_service = UserService(db)
    user = await user_service.get_by_id(int(user_id))
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    # Create new tokens
    access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
    )


@router.post("/logout")
async def logout(
    current_user: CurrentUser,
    db: DbSession,
    request_info: RequestInfo,
):
    """Logout user (logs the action for audit)."""
    audit_service = AuditService(db)
    
    await audit_service.log(
        action=AuditAction.logout,
        resource_type="auth",
        user_id=current_user.id,
        **request_info,
    )
    
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser):
    """Get current user information."""
    return UserResponse.model_validate(current_user)
