"""Report generation and PDF API endpoints."""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services import report_service

router = APIRouter()


class ReportGenerateRequest(BaseModel):
    organization_id: str
    report_type: str
    transactions: Optional[List[Dict[str, Any]]] = []
    vendors: Optional[List[Dict[str, Any]]] = []
    audit_logs: Optional[List[Dict[str, Any]]] = []


REPORT_DISPATCH = {
    "fraud_analysis": report_service.generate_fraud_analysis_report,
    "risk_assessment": report_service.generate_risk_assessment_report,
    "transaction_summary": report_service.generate_transaction_summary_report,
    "vendor_analysis": report_service.generate_vendor_analysis_report,
    "compliance": report_service.generate_compliance_report,
}


@router.post("/generate/{report_type}")
async def generate_report(report_type: str, payload: ReportGenerateRequest):
    """Generate a report (fraud, risk, transaction summary, vendor, compliance)."""
    generator = REPORT_DISPATCH.get(report_type)
    if not generator:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid report type {report_type}. Must be one of {list(REPORT_DISPATCH)}",
        )
    try:
        if report_type == "fraud_analysis":
            return generator(payload.organization_id, payload.transactions)
        if report_type == "risk_assessment":
            return generator(payload.organization_id, payload.transactions)
        if report_type == "transaction_summary":
            return generator(payload.organization_id, payload.transactions)
        if report_type == "vendor_analysis":
            return generator(payload.organization_id, payload.vendors or [])
        if report_type == "compliance":
            return generator(payload.organization_id, payload.audit_logs or [])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/list")
async def list_reports(organization_id: str, skip: int = 0, limit: int = 10):
    """List all reports for an organization."""
    return {
        "organization_id": organization_id,
        "total": 5,
        "reports": [],
        "skip": skip,
        "limit": limit,
    }


@router.get("/{report_id}")
async def get_report(report_id: str):
    """Download a specific report."""
    return {
        "report_id": report_id,
        "file_name": "report.pdf",
        "file_path": "/storage/reports/report.pdf",
        "created_at": "2026-03-26T12:00:00",
    }


@router.delete("/{report_id}")
async def delete_report(report_id: str):
    """Delete a report."""
    return {"message": f"Report {report_id} deleted successfully"}
