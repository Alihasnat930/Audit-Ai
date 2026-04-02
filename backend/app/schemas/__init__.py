"""Pydantic schemas for API requests and responses."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserSchema(BaseModel):
    user_id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    
    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: str = "auditor"


class OrganizationSchema(BaseModel):
    organization_id: str
    name: str
    industry: Optional[str] = None
    country: str
    currency: str
    
    class Config:
        from_attributes = True


class OrganizationCreateSchema(BaseModel):
    name: str
    industry: Optional[str] = None
    country: str
    currency: str = "USD"
