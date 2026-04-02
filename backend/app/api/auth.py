"""Authentication API endpoints."""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel


router = APIRouter()

DEMO_PASSWORD = "demo123456"
DEMO_USER = {
    "user_id": "demo-user-1",
    "organization_id": "demo-org",
    "email": "admin@auditai.com",
    "full_name": "AuditAI Demo Admin",
    "role": "admin",
    "is_active": True,
}


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    organization_id: str
    email: str
    full_name: str
    role: str


class UserCreateRequest(BaseModel):
    email: str
    full_name: str
    password: str
    role: str = "auditor"


class UserResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    role: str
    is_active: bool


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """Login endpoint returning demo credentials for the showcase app."""
    email = credentials.email.strip().lower()
    if email != DEMO_USER["email"] or credentials.password != DEMO_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid demo credentials",
        )

    return {
        "access_token": "demo-access-token",
        "token_type": "bearer",
        **{key: DEMO_USER[key] for key in LoginResponse.model_fields if key not in {"access_token", "token_type"}},
    }


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreateRequest):
    """Register a new user in demo mode."""
    return {
        "user_id": "demo-user-new",
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": user_data.role,
        "is_active": True,
    }


@router.post("/logout")
async def logout():
    """Logout endpoint."""
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """Get current authenticated user."""
    return {
        "user_id": DEMO_USER["user_id"],
        "email": DEMO_USER["email"],
        "full_name": DEMO_USER["full_name"],
        "role": DEMO_USER["role"],
        "is_active": DEMO_USER["is_active"],
    }
