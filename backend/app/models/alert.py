"""Alert model for high-risk transaction notifications."""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..db.base import Base


class AlertType(str, enum.Enum):
    HIGH_FRAUD_SCORE = "high_fraud_score"
    HIGH_RISK_SCORE = "high_risk_score"
    DUPLICATE_TRANSACTION = "duplicate_transaction"
    MISSING_INVOICE = "missing_invoice"
    UNUSUAL_VENDOR = "unusual_vendor"
    WEEKEND_ODD_TIME = "weekend_odd_time"


class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(String(36), primary_key=True, unique=True, index=True)
    transaction_id = Column(String(36), ForeignKey("transactions.transaction_id"), nullable=False, index=True)
    
    alert_type = Column(SQLEnum(AlertType), nullable=False, index=True)
    message = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False, default="medium")  # low, medium, high, critical
    
    resolved_flag = Column(Integer, nullable=False, default=0)  # 0 or 1
    resolved_by = Column(String(36), nullable=True)  # user_id who resolved
    resolved_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transaction = relationship("Transaction", back_populates="alerts")
