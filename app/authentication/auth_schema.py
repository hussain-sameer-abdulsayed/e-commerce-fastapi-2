from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber
PhoneNumber.phone_format = 'E164'
from uuid import UUID
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    SELLER = "seller"
    ADMIN = "admin"


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None


class LoginRequestEmail(BaseModel):
    email: EmailStr
    password: str


class LoginRequestPhone(BaseModel):
    phone: PhoneNumber
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    full_name: str
    phone_number: Optional[str] = None
    role: UserRole = UserRole.USER


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6, max_length=100)


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=6, max_length=100)


class AuthResponse(BaseModel):
    user_id: UUID
    email: str
    full_name: str
    role: UserRole
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


