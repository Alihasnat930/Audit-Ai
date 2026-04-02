"""AI/LLM service for explanations, summarizations, and chatbot responses."""
import logging
from typing import Any, Dict, Optional

from ..ai.llm.chatbot import build_chatbot_prompt, extract_sources
from ..ai.llm.explanation import (
    build_explain_prompt,
    extract_fraud_indicators,
    extract_recommendations,
    extract_risk_factors,
)
from ..ai.llm.summary import build_summary_prompt, extract_findings
from ..config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def explain_transaction(transaction_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate explanation for transaction fraud/risk indicators using LLM."""
    try:
        prompt = build_explain_prompt(transaction_data)
        response = call_llm(prompt, model="gpt-4", max_tokens=500)
        
        return {
            "transaction_id": transaction_data.get("transaction_id"),
            "summary": response.get("text", ""),
            "confidence": response.get("confidence", 0.7),
            "risk_factors": extract_risk_factors(response.get("text", "")),
            "fraud_indicators": extract_fraud_indicators(response.get("text", "")),
            "recommendations": extract_recommendations(response.get("text", ""))
        }
    except Exception as e:
        logger.error(f"Error explaining transaction: {e}")
        return {
            "transaction_id": transaction_data.get("transaction_id"),
            "summary": "Unable to generate explanation at this time.",
            "confidence": 0.0,
            "risk_factors": [],
            "fraud_indicators": [],
            "recommendations": []
        }


def summarize_transactions(organization_data: Dict[str, Any], period: str = "7d") -> Dict[str, Any]:
    """Generate summary of audit findings for organization."""
    try:
        prompt = build_summary_prompt(organization_data, period)
        response = call_llm(prompt, model="gpt-4", max_tokens=800)
        
        return {
            "summary": response.get("text", ""),
            "confidence": response.get("confidence", 0.7),
            "key_findings": extract_findings(response.get("text", "")),
            "alerts": organization_data.get("alerts", []),
            "period": period
        }
    except Exception as e:
        logger.error(f"Error summarizing transactions: {e}")
        return {
            "summary": "Unable to generate summary at this time.",
            "confidence": 0.0,
            "key_findings": [],
            "alerts": organization_data.get("alerts", []),
            "period": period
        }


def answer_chatbot_question(question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Answer user questions about audit findings using LLM."""
    try:
        prompt = build_chatbot_prompt(question, context)
        response = call_llm(prompt, model="gpt-4", max_tokens=500)
        
        return {
            "question": question,
            "answer": response.get("text", ""),
            "confidence": response.get("confidence", 0.7),
            "sources": extract_sources(response.get("text", ""))
        }
    except Exception as e:
        logger.error(f"Error answering chatbot question: {e}")
        return {
            "question": question,
            "answer": "I'm sorry, I couldn't generate an answer at this time. Please try again.",
            "confidence": 0.0,
            "sources": []
        }


def call_llm(prompt: str, model: str = None, max_tokens: int = 500) -> Dict[str, Any]:
    """Call LLM API (OpenRouter/HuggingFace/OpenAI).
    
    Returns: {"text": response_text, "confidence": 0.0-1.0}
    """
    try:
        if not settings.openrouter_api_key and not settings.openai_api_key:
            logger.warning("No LLM API keys configured; returning mock response")
            return {
                "text": "Mock LLM response. Configure OpenRouter or OpenAI API for real responses.",
                "confidence": 0.5
            }
        
        # If using OpenRouter
        if settings.openrouter_api_key:
            return _call_openrouter(prompt, model, max_tokens)
        
        # If using OpenAI
        if settings.openai_api_key:
            return _call_openai(prompt, model, max_tokens)
        
        return {"text": "", "confidence": 0.0}
    except Exception as e:
        logger.error(f"Error calling LLM: {e}")
        return {"text": "", "confidence": 0.0}


def _call_openrouter(prompt: str, model: str, max_tokens: int) -> Dict[str, Any]:
    """Call OpenRouter API."""
    try:
        import requests
        # Use default model if not specified
        if not model:
            model = settings.openrouter_default_model
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "HTTP-Referer": "https://auditai.local",
                "X-Title": "AuditAI"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"]
        return {"text": text, "confidence": 0.9}
    except Exception as e:
        logger.error(f"Error calling OpenRouter: {e}")
        return {"text": "", "confidence": 0.0}


def _call_openai(prompt: str, model: str, max_tokens: int) -> Dict[str, Any]:
    """Call OpenAI API."""
    try:
        import requests
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model or "gpt-4",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"]
        return {"text": text, "confidence": 0.9}
    except Exception as e:
        logger.error(f"Error calling OpenAI: {e}")
        return {"text": "", "confidence": 0.0}
