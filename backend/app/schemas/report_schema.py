"""Report schemas for API requests/responses."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReportSchema(BaseModel):
    report_id: str
    organization_id: str
    report_type: str
    title: str
    description: Optional[str] = None
    file_name: str
    file_path: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReportCreateSchema(BaseModel):
    report_type: str
    title: str
    description: Optional[str] = None
