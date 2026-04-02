"""Organization model for multi-tenant enterprise data."""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from ..db.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    organization_id = Column(String(36), primary_key=True, unique=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    industry = Column(String(255), nullable=True)
    country = Column(String(100), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="organization")
    vendors = relationship("Vendor", back_populates="organization")
    transactions = relationship("Transaction", back_populates="organization")
    reports = relationship("Report", back_populates="organization")
    audit_logs = relationship("AuditLog", back_populates="organization")
