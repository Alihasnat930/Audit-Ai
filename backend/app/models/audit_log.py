"""Audit log model for compliance and activity tracking."""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from ..db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(String(36), primary_key=True, unique=True, index=True)
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False, index=True)
    organization_id = Column(String(36), ForeignKey("organizations.organization_id"), nullable=False, index=True)
    
    action_type = Column(String(100), nullable=False)  # create, update, delete, view, export, etc.
    target_table = Column(String(100), nullable=False)  # transactions, reports, etc.
    target_id = Column(String(36), nullable=False)  # ID of the affected record
    
    details = Column(Text, nullable=True)  # JSON or text description of changes
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
    organization = relationship("Organization", back_populates="audit_logs")
