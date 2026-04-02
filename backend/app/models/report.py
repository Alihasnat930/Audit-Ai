"""Report model for audit findings and compliance."""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..db.base import Base


class ReportType(str, enum.Enum):
    TRANSACTION_SUMMARY = "transaction_summary"
    FRAUD_ANALYSIS = "fraud_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    VENDOR_ANALYSIS = "vendor_analysis"
    COMPLIANCE = "compliance"


class Report(Base):
    __tablename__ = "reports"

    report_id = Column(String(36), primary_key=True, unique=True, index=True)
    organization_id = Column(String(36), ForeignKey("organizations.organization_id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.user_id"), nullable=False)
    
    report_type = Column(SQLEnum(ReportType), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)  # S3 or local path
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="reports")
    user = relationship("User")
