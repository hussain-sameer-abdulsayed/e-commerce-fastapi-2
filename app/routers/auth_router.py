from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from app.db.database import get_db
from app.models.user import User
from app.services.auth_service import AuthService
from app.authentication.auth_schema import (
    LoginRequestEmail, RegisterRequest, RefreshTokenRequest,
    ChangePasswordRequest, AuthResponse, Token
)
from app.schemas.user import UserRead
from app.authentication.auth_dependency import get_current_active_user, get_current_verified_user

router = APIRouter(
    responses= {404 : {"description":"Not found"}}
)


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    register_data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account.
    
    - **email**: Valid email address (unique)
    - **password**: Password (min 6 characters)
    - **full_name**: User's full name
    - **phone_number**: Optional phone number
    - **role**: User role (user, seller, admin) - defaults to 'user'
    """
    service = AuthService(db)
    return await service.register(register_data)


@router.post("/login", response_model=AuthResponse)
async def login(
    login_data: LoginRequestEmail,
    db: AsyncSession = Depends(get_db)
):
    """
    Login with email and password.
    
    Returns access token and refresh token.
    """
    service = AuthService(db)
    return await service.login(login_data)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    """
    service = AuthService(db)
    return await service.refresh_token(refresh_data)


@router.post("/logout", response_model=Dict[str, str])
async def logout(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout current user by revoking refresh token.
    """
    service = AuthService(db)
    success = await service.logout(current_user.id)
    
    if success:
        return {"message": "Successfully logged out"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to logout"
        )


@router.post("/change-password", response_model=Dict[str, str])
async def change_password(
    change_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Change password for current user.
    
    - **old_password**: Current password
    - **new_password**: New password (min 6 characters)
    """
    service = AuthService(db)
    success = await service.change_password(current_user.id, change_data)
    
    if success:
        return {"message": "Password changed successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )


@router.get("/me", response_model=UserRead)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user information.
    """
    return UserRead(
        id=current_user.id,
        user_name=current_user.user_name,
        full_name=current_user.full_name,
        email=current_user.email,
        phone_number=current_user.phone_number or "",
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )


@router.post("/verify-email", response_model=Dict[str, str])
async def verify_email(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Verify email for current user.
    
    In a real application, this would involve sending a verification email
    with a token. For now, this directly verifies the user.
    """
    service = AuthService(db)
    success = await service.verify_user_email(current_user.id)
    
    if success:
        return {"message": "Email verified successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify email"
        )


