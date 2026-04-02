"""Transaction model for enterprise audit data."""
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..db.base import Base


class RiskLevel(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String(36), primary_key=True, unique=True, index=True)
    organization_id = Column(String(36), ForeignKey("organizations.organization_id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    vendor_id = Column(String(36), ForeignKey("vendors.vendor_id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    category = Column(String(100), nullable=False)
    payment_method = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    
    # ML predictions
    anomaly_flag = Column(Integer, nullable=False, default=0)  # 0 or 1
    fraud_score = Column(Float, nullable=False, default=0.0)  # 0-1
    risk_score = Column(Float, nullable=False, default=0.0)  # 0-100
    risk_level = Column(SQLEnum(RiskLevel), nullable=False, default=RiskLevel.LOW)
    
    # Rule-based flags
    duplicate_flag = Column(Integer, nullable=False, default=0)
    missing_invoice_flag = Column(Integer, nullable=False, default=0)
    unusual_vendor_flag = Column(Integer, nullable=False, default=0)
    weekend_or_odd_time_flag = Column(Integer, nullable=False, default=0)
    
    source_file_id = Column(String(36), nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="transactions")
    vendor = relationship("Vendor", back_populates="transactions")
    user = relationship("User")
    documents = relationship("Document", back_populates="transaction")
    alerts = relationship("Alert", back_populates="transaction")
