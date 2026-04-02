"""User model for authentication and authorization."""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..db.base import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    AUDITOR = "auditor"
    FINANCE = "finance"


class User(Base):
    __tablename__ = "users"

    user_id = Column(String(36), primary_key=True, unique=True, index=True)
    organization_id = Column(String(36), ForeignKey("organizations.organization_id"), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.AUDITOR)
    is_active = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="users")
    audit_logs = relationship("AuditLog", back_populates="user")
