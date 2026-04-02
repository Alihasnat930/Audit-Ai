from typing import Any, Dict, List

_FINDING_KEYWORDS = ["finding", "discovered", "identified", "found", "notable", "highlight"]


def build_summary_prompt(org_data: Dict[str, Any], period: str) -> str:
    return f"""Summarize audit findings for organization {org_data.get('organization_id')} for period {period}:
Total Transactions: {org_data.get('total_transactions', 0)}
High Risk Count: {org_data.get('high_risk_count', 0)}
Fraud Detections: {org_data.get('fraud_detections', 0)}
Average Fraud Score: {org_data.get('avg_fraud_score', 0):.2f}
Average Risk Score: {org_data.get('avg_risk_score', 0):.2f}

Provide:
1. Executive summary
2. Key findings
3. Risk assessment
4. Recommendations
"""


def _extract_sentences(text: str) -> List[str]:
    return [sentence.strip() for sentence in text.split(".") if sentence.strip()]


def extract_findings(text: str) -> List[str]:
    return [sentence for sentence in _extract_sentences(text) if any(keyword in sentence.lower() for keyword in _FINDING_KEYWORDS)][:10]
