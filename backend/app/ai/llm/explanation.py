from typing import Any, Dict, List

_SUMMARY_TEMPLATE = """
Analyze this financial transaction and explain fraud/risk indicators.
Amount: ${amount}
Vendor: {vendor}
Category: {category}
Fraud Score: {fraud_score}
Risk Score: {risk_score}
{details_block}
Provide:
1. Summary
2. Risk factors
3. Fraud indicators
4. Recommendations
Save the response as JSON with sections.
"""

_RISK_KEYWORDS = ["unusual", "high", "anomaly", "suspicious", "red flag"]
_FRAUD_KEYWORDS = ["fraud", "duplicate", "missing invoice", "unusual vendor", "weekend"]
_RECOMMEND_KEYWORDS = ["recommend", "should", "must", "investigate", "review", "validate"]


def build_explain_prompt(transaction_data: Dict[str, Any]) -> str:
    details = transaction_data.get("details", {})
    formatted_details = "\n".join(f"{k}: {v}" for k, v in details.items()) if details else "No additional details provided."
    return _SUMMARY_TEMPLATE.format(
        amount=transaction_data.get("amount", 0),
        vendor=transaction_data.get("vendor", "Unknown"),
        category=transaction_data.get("category", "Unknown"),
        fraud_score=transaction_data.get("fraud_score", 0),
        risk_score=transaction_data.get("risk_score", 0),
        details_block=formatted_details,
    )


def _extract_sentences(text: str) -> List[str]:
    return [sentence.strip() for sentence in text.split(".") if sentence.strip()]


def _find_keywords(text: str, keywords: List[str]) -> List[str]:
    return [sentence for sentence in _extract_sentences(text) if any(keyword in sentence.lower() for keyword in keywords)]


def extract_risk_factors(text: str) -> List[str]:
    return _find_keywords(text, _RISK_KEYWORDS)[:5]


def extract_fraud_indicators(text: str) -> List[str]:
    return _find_keywords(text, _FRAUD_KEYWORDS)[:5]


def extract_recommendations(text: str) -> List[str]:
    return _find_keywords(text, _RECOMMEND_KEYWORDS)[:5]
