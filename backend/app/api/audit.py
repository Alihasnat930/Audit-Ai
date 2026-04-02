"""Audit processing and ML model API endpoints."""
import logging
import os
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..services.audit_service import orchestrate_audit
from ..services.data_service import (
    build_dashboard_summary,
    build_monthly_trends,
    get_risk_distribution,
    get_recent_alerts,
    get_sample_transactions,
    get_vendor_risk_summary,
)

router = APIRouter()
logger = logging.getLogger(__name__)


class AuditRunRequest(BaseModel):
    organization_id: str
    file_path: str



@router.post("/run")
async def run_audit(payload: AuditRunRequest):
    """Run fraud/risk scoring on the referenced upload."""
    logger.info(f"Running audit on {payload.file_path} for org {payload.organization_id}")
    if not os.path.isfile(payload.file_path):
        raise HTTPException(status_code=400, detail="File path does not exist")
    result = orchestrate_audit(payload.file_path, payload.organization_id)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
    return result


@router.get("/transactions")
async def get_transactions(
    organization_id: str,
    risk_level: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    """Get transactions with optional filtering by risk level (Low, Medium, High)."""
    transactions = get_sample_transactions(
        organization_id,
        risk_level=risk_level,
        skip=skip,
        limit=limit,
    )
    return {
        "total": len(transactions),
        "skip": skip,
        "limit": limit,
        "transactions": transactions,
        "risk_level_filter": risk_level
    }


@router.get("/transaction/{transaction_id}")
async def get_transaction_detail(transaction_id: str):
    """Get detailed analysis of a specific transaction."""
    return {
        "transaction_id": transaction_id,
        "fraud_score": 0.25,
        "risk_score": 35.5,
        "risk_level": "Low",
        "explanations": []
    }


@router.get("/summary")
async def get_audit_summary(organization_id: str):
    """Get summary statistics for the organization's audit."""
    summary = build_dashboard_summary(organization_id)
    trends = build_monthly_trends(organization_id)
    risk_dist = get_risk_distribution(organization_id)
    alerts = get_recent_alerts(organization_id)
    return {
        "organization_id": organization_id,
        "summary": summary,
        "trends": trends,
        "risk_distribution": risk_dist,
        "alerts": alerts,
    }


@router.get("/vendors")
async def get_vendor_risks(organization_id: str):
    """Get vendor risk analysis."""
    vendors = get_vendor_risk_summary(organization_id)
    return {
        "organization_id": organization_id,
        "vendors": vendors
    }


@router.get("/alerts")
async def get_alerts(organization_id: str, limit: int = 10):
    """Stream recent alerts sorted by fraud and risk score."""
    alerts = get_recent_alerts(organization_id, limit=limit)
    return {
        "organization_id": organization_id,
        "alerts": alerts,
        "count": len(alerts),
        "limit": limit,
    }
