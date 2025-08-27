from typing import Optional, List
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.authentication.auth_schema import UserRole
from app.db.database import get_db
from app.models.user import User
from app.repositories.auth_repository import AuthRepository
from .auth_configuration import decode_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    
    # Decode token
    payload = decode_token(token)
    
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    auth_repo = AuthRepository(db)
    user = await auth_repo.get_user_by_id(UUID(user_id))
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current verified user."""
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email first"
        )
    return current_user


class RoleChecker:
    """Role-based access control dependency."""
    
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, user: User = Depends(get_current_active_user)) -> User:
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with role '{user.role.value}' is not authorized to access this resource"
            )
        return user


# Pre-configured role checkers
require_admin = RoleChecker([UserRole.ADMIN])
require_seller = RoleChecker([UserRole.SELLER, UserRole.ADMIN])
require_seller_only = RoleChecker([UserRole.SELLER])
require_user = RoleChecker([UserRole.USER, UserRole.SELLER, UserRole.ADMIN])


async def get_optional_current_user(
    authorization: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """Get current user if token is provided, otherwise return None."""
    if not authorization:
        return None
    
    try:
        # Extract token from Bearer scheme
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        
        # Decode token
        payload = decode_token(token)
        
        if not payload or payload.get("type") != "access":
            return None
        
        user_id = payload.get("sub")
        if user_id is None:
            return None
        
        # Get user from database
        auth_repo = AuthRepository(db)
        user = await auth_repo.get_user_by_id(UUID(user_id))
        
        if user and user.is_active:
            return user
        
    except (ValueError, JWTError):
        pass
    
    return None