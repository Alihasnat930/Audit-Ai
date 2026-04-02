"""AI Chatbot API for explaining risks and fraud findings."""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from ..services.ai_service import (
    answer_chatbot_question,
    explain_transaction,
    summarize_transactions,
)

router = APIRouter()


class ChatMessageRequest(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None


class ExplainRequest(BaseModel):
    transaction_id: str
    amount: float
    vendor: Optional[str] = None
    category: Optional[str] = None
    fraud_score: float = 0.0
    risk_score: float = 0.0
    details: Optional[Dict[str, Any]] = None


class SummaryRequest(BaseModel):
    organization_id: str
    total_transactions: int = 0
    high_risk_count: int = 0
    fraud_detections: int = 0
    avg_fraud_score: float = 0.0
    avg_risk_score: float = 0.0
    alerts: Optional[List[Dict[str, Any]]] = []
    period: str = "week"


@router.post("/message")
async def chat_message(request: ChatMessageRequest):
    """Send a message to the AI chatbot and get a response."""
    return answer_chatbot_question(request.question, context=request.context)


@router.post("/explain")
async def explain_transaction_endpoint(request: ExplainRequest):
    """Get AI-generated explanation of transaction risk/fraud."""
    payload = {
        "transaction_id": request.transaction_id,
        "amount": request.amount,
        "vendor": request.vendor,
        "category": request.category,
        "fraud_score": request.fraud_score,
        "risk_score": request.risk_score,
        "details": request.details or {},
    }
    return explain_transaction(payload)


@router.post("/summarize")
async def summarize_transactions_endpoint(request: SummaryRequest):
    """Get AI-generated summary of transactions for a time period."""
    organization_data = {
        "organization_id": request.organization_id,
        "total_transactions": request.total_transactions,
        "high_risk_count": request.high_risk_count,
        "fraud_detections": request.fraud_detections,
        "avg_fraud_score": request.avg_fraud_score,
        "avg_risk_score": request.avg_risk_score,
        "alerts": request.alerts or [],
    }
    return summarize_transactions(organization_data, period=request.period)
