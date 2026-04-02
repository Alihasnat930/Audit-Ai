"""Transaction schemas for API requests/responses."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TransactionSchema(BaseModel):
    transaction_id: str
    organization_id: str
    amount: float
    currency: str
    category: str
    payment_method: str
    anomaly_flag: int
    fraud_score: float
    risk_score: float
    risk_level: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TransactionCreateSchema(BaseModel):
    amount: float
    currency: str
    category: str
    payment_method: str
    vendor_id: str
    description: Optional[str] = None


class TransactionDetailSchema(TransactionSchema):
    vendor_id: str
    user_id: str
    description: Optional[str] = None
    duplicate_flag: int
    missing_invoice_flag: int
    unusual_vendor_flag: int
    weekend_or_odd_time_flag: int
