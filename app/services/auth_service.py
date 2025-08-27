from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from app.authentication.auth_schema import (
    LoginRequestEmail, LoginRequestPhone, RegisterRequest, RefreshTokenRequest,
    ChangePasswordRequest, AuthResponse, Token, UserRole
)
from app.authentication.auth_configuration import (
    verify_password, get_password_hash, create_tokens,
    decode_token, create_access_token, create_refresh_token
)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = AuthRepository(db)
    
    

    async def register(self, register_data: RegisterRequest) -> AuthResponse:
        """Register a new user."""
        # Check if email already exists
        if await self.repository.check_email_exists(register_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if phone already exists (if provided)
        if register_data.phone_number:
            if await self.repository.check_phone_exists(register_data.phone_number):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number already registered"
                )
        
        # Create new user
        user = User(
            email=register_data.email,
            full_name=register_data.full_name,
            phone_number=register_data.phone_number,
            password_hash=get_password_hash(register_data.password),
            role=register_data.role
        )
        
        # Save user to database
        created_user = await self.repository.create_user(user)
        
        # Generate tokens
        tokens = create_tokens(
            user_id=str(created_user.id),
            email=created_user.email,
            role=created_user.role.value
        )
        
        # Save refresh token
        await self.repository.save_refresh_token(
            created_user.id,
            tokens["refresh_token"]
        )
        
        return AuthResponse(
            user_id=created_user.id,
            email=created_user.email,
            full_name=created_user.full_name,
            role=created_user.role,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"]
        )
    

    async def login(self, login_data: LoginRequestEmail) -> AuthResponse:
        """Authenticate user and return tokens."""
        # Get user by email
        user = await self.repository.get_user_by_email(login_data.email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Generate tokens
        tokens = create_tokens(
            user_id=str(user.id),
            email=user.email,
            role=user.role.value
        )
        
        # Save refresh token
        await self.repository.save_refresh_token(
            user.id,
            tokens["refresh_token"]
        )
        
        return AuthResponse(
            user_id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"]
        )
    

    async def refresh_token(self, refresh_data: RefreshTokenRequest) -> Token:
        """Refresh access token using refresh token."""
        # Decode refresh token
        payload = decode_token(refresh_data.refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get user from refresh token
        user = await self.repository.get_user_by_refresh_token(refresh_data.refresh_token)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Generate new tokens
        tokens = create_tokens(
            user_id=str(user.id),
            email=user.email,
            role=user.role.value
        )
        
        # Save new refresh token
        await self.repository.save_refresh_token(
            user.id,
            tokens["refresh_token"]
        )
        
        return Token(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"]
        )
    

    async def logout(self, user_id: UUID) -> bool:
        """Logout user by revoking refresh token."""
        return await self.repository.revoke_refresh_token(user_id)
    

    async def change_password(self, user_id: UUID, change_data: ChangePasswordRequest) -> bool:
        """Change user password."""
        # Get user
        user = await self.repository.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify old password
        if not verify_password(change_data.old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid old password"
            )
        
        # Update password
        user.password_hash = get_password_hash(change_data.new_password)
        await self.repository.update_user(user)
        
        # Revoke refresh token to force re-login
        await self.repository.revoke_refresh_token(user_id)
        
        return True
    

    async def get_current_user(self, user_id: UUID) -> User:
        """Get current user information."""
        user = await self.repository.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        return user
    

    async def verify_user_email(self, user_id: UUID) -> bool:
        """Verify user email address."""
        return await self.repository.verify_user(user_id)
    

