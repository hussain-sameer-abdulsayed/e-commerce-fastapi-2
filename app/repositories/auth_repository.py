from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        statement = select(User).where(User.email == email)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        statement = select(User).where(User.id == user_id)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    

    async def create_user(self, user: User) -> User:
        """Create a new user."""
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    

    async def update_user(self, user: User) -> User:
        """Update user information."""
        user.updated_at = datetime.utcnow()
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    

    async def save_refresh_token(self, user_id: UUID, refresh_token: str) -> bool:
        """Save refresh token for a user."""
        user = await self.get_user_by_id(user_id)
        if user:
            user.refresh_token = refresh_token
            await self.update_user(user)
            return True
        return False
    

    async def get_user_by_refresh_token(self, refresh_token: str) -> Optional[User]:
        """Get user by refresh token."""
        statement = select(User).where(User.refresh_token == refresh_token)
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()
    

    async def revoke_refresh_token(self, user_id: UUID) -> bool:
        """Revoke user's refresh token."""
        user = await self.get_user_by_id(user_id)
        if user:
            user.refresh_token = None
            await self.update_user(user)
            return True
        return False
    

    async def verify_user(self, user_id: UUID) -> bool:
        """Mark user as verified."""
        user = await self.get_user_by_id(user_id)
        if user:
            user.is_verified = True
            await self.update_user(user)
            return True
        return False
    

    async def check_email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        statement = select(User).where(User.email == email)
        result = await self.db.execute(statement)
        return result.first() is not None
    
    
    async def check_phone_exists(self, phone: str) -> bool:
        """Check if phone number already exists."""
        statement = select(User).where(User.phone_number == phone)
        result = await self.db.execute(statement)
        return result.first() is not None
    


