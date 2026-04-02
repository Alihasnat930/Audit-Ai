"""Vendor model for transaction counterparties."""
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..db.base import Base


class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id = Column(String(36), primary_key=True, unique=True, index=True)
    organization_id = Column(String(36), ForeignKey("organizations.organization_id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    industry = Column(String(255), nullable=True)
    country = Column(String(100), nullable=False)
    risk_score = Column(Float, nullable=False, default=0.0)  # Pre-computed vendor risk 0-1
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="vendors")
    transactions = relationship("Transaction", back_populates="vendor")
