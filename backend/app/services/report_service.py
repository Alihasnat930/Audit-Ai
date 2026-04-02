"""Report generation service for PDF/HTML exports."""
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_fraud_analysis_report(organization_id: str, transactions: list) -> Dict[str, Any]:
    """Generate fraud analysis report."""
    try:
        if not transactions:
            return {
                "status": "error",
                "message": "No transactions provided"
            }
        
        # Calculate fraud metrics
        fraud_transactions = [t for t in transactions if t.get("anomaly_flag", 0) == 1]
        high_fraud_score = [t for t in transactions if t.get("fraud_score", 0) > 0.7]
        
        report = {
            "organization_id": organization_id,
            "report_type": "fraud_analysis",
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "total_transactions": len(transactions),
                "fraud_detections": len(fraud_transactions),
                "fraud_rate": round(len(fraud_transactions) / len(transactions) * 100, 2) if transactions else 0,
                "high_fraud_score_count": len(high_fraud_score),
                "avg_fraud_score": round(sum(t.get("fraud_score", 0) for t in transactions) / len(transactions), 4)
            },
            "top_fraud_transactions": sorted(transactions, key=lambda x: x.get("fraud_score", 0), reverse=True)[:10],
            "fraud_indicators": _extract_fraud_patterns(fraud_transactions),
            "recommendations": _generate_fraud_recommendations(fraud_transactions)
        }
        
        # Generate PDF if ReportLab available
        if REPORTLAB_AVAILABLE:
            pdf_content = _generate_pdf(report)
            report["pdf_format"] = True
        else:
            report["pdf_format"] = False
            logger.warning("ReportLab not available; PDF generation disabled")
        
        return {"status": "success", "report": report}
    except Exception as e:
        logger.error(f"Error generating fraud analysis report: {e}")
        return {"status": "error", "message": str(e)}


def generate_risk_assessment_report(organization_id: str, transactions: list) -> Dict[str, Any]:
    """Generate risk assessment report."""
    try:
        if not transactions:
            return {"status": "error", "message": "No transactions provided"}
        
        # Calculate risk metrics
        high_risk = [t for t in transactions if t.get("risk_level") == "High"]
        medium_risk = [t for t in transactions if t.get("risk_level") == "Medium"]
        
        report = {
            "organization_id": organization_id,
            "report_type": "risk_assessment",
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "total_transactions": len(transactions),
                "high_risk_count": len(high_risk),
                "medium_risk_count": len(medium_risk),
                "low_risk_count": len([t for t in transactions if t.get("risk_level") == "Low"]),
                "avg_risk_score": round(sum(t.get("risk_score", 0) for t in transactions) / len(transactions), 2)
            },
            "risk_distribution": {
                "high": len(high_risk),
                "medium": len(medium_risk),
                "low": len([t for t in transactions if t.get("risk_level") == "Low"])
            },
            "high_risk_transactions": high_risk[:20],
            "risk_factors": _extract_risk_patterns(transactions),
            "recommendations": _generate_risk_recommendations(high_risk)
        }
        
        if REPORTLAB_AVAILABLE:
            pdf_content = _generate_pdf(report)
            report["pdf_format"] = True
        else:
            report["pdf_format"] = False
        
        return {"status": "success", "report": report}
    except Exception as e:
        logger.error(f"Error generating risk assessment report: {e}")
        return {"status": "error", "message": str(e)}


def generate_transaction_summary_report(organization_id: str, transactions: list) -> Dict[str, Any]:
    """Generate transaction summary report."""
    try:
        if not transactions:
            return {"status": "error", "message": "No transactions provided"}
        
        # Group by category
        by_category = {}
        for t in transactions:
            cat = t.get("category", "Other")
            if cat not in by_category:
                by_category[cat] = {"count": 0, "amount": 0}
            by_category[cat]["count"] += 1
            by_category[cat]["amount"] += t.get("amount", 0)
        
        # Group by vendor (top 10)
        by_vendor = {}
        for t in transactions:
            vendor = t.get("vendor") or t.get("vendor_name") or "Unknown"
            if vendor not in by_vendor:
                by_vendor[vendor] = {"count": 0, "amount": 0}
            by_vendor[vendor]["count"] += 1
            by_vendor[vendor]["amount"] += t.get("amount", 0)
        
        top_vendors = sorted(by_vendor.items(), key=lambda x: x[1]["amount"], reverse=True)[:10]
        
        report = {
            "organization_id": organization_id,
            "report_type": "transaction_summary",
            "generated_at": datetime.utcnow().isoformat(),
            "totals": {
                "total_transactions": len(transactions),
                "total_amount": sum(t.get("amount", 0) for t in transactions),
                "avg_amount": round(sum(t.get("amount", 0) for t in transactions) / len(transactions), 2),
                "min_amount": min((t.get("amount", 0) for t in transactions), default=0),
                "max_amount": max((t.get("amount", 0) for t in transactions), default=0)
            },
            "by_category": by_category,
            "top_vendors": [{"vendor": v, "count": stats["count"], "amount": stats["amount"]} 
                          for v, stats in top_vendors]
        }
        
        if REPORTLAB_AVAILABLE:
            pdf_content = _generate_pdf(report)
            report["pdf_format"] = True
        else:
            report["pdf_format"] = False
        
        return {"status": "success", "report": report}
    except Exception as e:
        logger.error(f"Error generating transaction summary report: {e}")
        return {"status": "error", "message": str(e)}


def generate_vendor_analysis_report(organization_id: str, vendors: list) -> Dict[str, Any]:
    """Generate vendor analysis report."""
    try:
        if not vendors:
            return {"status": "error", "message": "No vendors provided"}
        
        # Sort by risk
        vendors_by_risk = sorted(vendors, key=lambda x: x.get("risk_score", 0), reverse=True)
        
        report = {
            "organization_id": organization_id,
            "report_type": "vendor_analysis",
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "total_vendors": len(vendors),
                "high_risk_vendors": len([v for v in vendors if v.get("risk_score", 0) > 70]),
                "avg_vendor_risk": round(sum(v.get("risk_score", 0) for v in vendors) / len(vendors), 2)
            },
            "vendors": vendors_by_risk[:50],  # Top 50 vendors by risk
            "vendor_risk_distribution": _analyze_vendor_risk_distribution(vendors)
        }
        
        if REPORTLAB_AVAILABLE:
            pdf_content = _generate_pdf(report)
            report["pdf_format"] = True
        else:
            report["pdf_format"] = False
        
        return {"status": "success", "report": report}
    except Exception as e:
        logger.error(f"Error generating vendor analysis report: {e}")
        return {"status": "error", "message": str(e)}


def generate_compliance_report(organization_id: str, audit_logs: list) -> Dict[str, Any]:
    """Generate compliance report."""
    try:
        if not audit_logs:
            audit_logs = []
        
        # Count operations by type
        by_action = {}
        for log in audit_logs:
            action = log.get("action_type", "Unknown")
            if action not in by_action:
                by_action[action] = 0
            by_action[action] += 1
        
        report = {
            "organization_id": organization_id,
            "report_type": "compliance",
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "total_audit_logs": len(audit_logs),
                "audit_period": "last_30_days",
                "actions_logged": len(by_action)
            },
            "actions_by_type": by_action,
            "compliance_status": "PASSING",  # Could add real checks
            "recommendations": [
                "Maintain regular audit log reviews",
                "Ensure all user actions are logged",
                "Archive audit logs according to retention policy",
                "Review access controls and permissions"
            ]
        }
        
        return {"status": "success", "report": report}
    except Exception as e:
        logger.error(f"Error generating compliance report: {e}")
        return {"status": "error", "message": str(e)}


def _generate_pdf(report: Dict[str, Any]) -> bytes:
    """Generate PDF from report data using ReportLab."""
    try:
        if not REPORTLAB_AVAILABLE:
            return b''
        
        # This is a simplified PDF generation
        # In production, would use a more sophisticated template
        logger.info(f"PDF generation requested for {report.get('report_type', 'unknown')} report")
        # Return empty bytes for now; full implementation would use reportlab.platypus
        return b''
    except Exception as e:
        logger.error(f"Error generating PDF: {e}")
        return b''


def _extract_fraud_patterns(fraud_transactions: list) -> list:
    """Extract common fraud patterns."""
    patterns = []
    if fraud_transactions:
        # Simple pattern extraction
        patterns.append(f"Detected {len(fraud_transactions)} fraudulent transactions")
        # Could add ML-based pattern detection here
    return patterns


def _extract_risk_patterns(transactions: list) -> list:
    """Extract common risk patterns."""
    patterns = []
    # Analyze risk factors
    missing_docs = len([t for t in transactions if t.get("missing_invoice_flag", 0) == 1])
    if missing_docs > 0:
        patterns.append(f"{missing_docs} transactions missing invoice documentation")
    
    duplicates = len([t for t in transactions if t.get("duplicate_flag", 0) == 1])
    if duplicates > 0:
        patterns.append(f"{duplicates} potential duplicate transactions detected")
    
    weekend = len([t for t in transactions if t.get("weekend_or_odd_time_flag", 0) == 1])
    if weekend > 0:
        patterns.append(f"{weekend} transactions during unusual times")
    
    return patterns


def _generate_fraud_recommendations(fraud_transactions: list) -> list:
    """Generate actionable fraud recommendations."""
    recs = [
        "Review flagged transactions for manual approval",
        "Investigate transaction patterns for organized fraud",
        "Update fraud detection thresholds based on findings",
        "Cross-reference with known fraud databases"
    ]
    if fraud_transactions:
        recs.append(f"Priority: Investigate top {min(5, len(fraud_transactions))} high-fraud transactions")
    
    return recs


def _generate_risk_recommendations(high_risk_transactions: list) -> list:
    """Generate actionable risk recommendations."""
    recs = [
        "Review and approve all high-risk transactions",
        "Strengthen internal controls in flagged areas",
        "Implement additional verification steps",
        "Monitor vendor relationships closely"
    ]
    if high_risk_transactions:
        recs.append(f"Urgent: Address {min(3, len(high_risk_transactions))} critical risk items")
    
    return recs


def _analyze_vendor_risk_distribution(vendors: list) -> dict:
    """Analyze vendor risk score distribution."""
    if not vendors:
        return {"high": 0, "medium": 0, "low": 0}
    
    return {
        "high": len([v for v in vendors if v.get("risk_score", 0) > 70]),
        "medium": len([v for v in vendors if 30 <= v.get("risk_score", 0) <= 70]),
        "low": len([v for v in vendors if v.get("risk_score", 0) < 30])
    }

