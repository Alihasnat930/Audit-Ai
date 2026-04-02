"""Audit orchestration service - coordinates ML models and rule-based detection."""
import logging
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from .data_service import parse_csv, clean_data, validate_transactions
from .fraud_service import predict_fraud
from .risk_service import score_risk
from .ocr_service import extract_text_from_file

logger = logging.getLogger(__name__)


def orchestrate_audit(file_path: str, organization_id: str) -> Dict[str, Any]:
    """Run complete audit pipeline: parse, validate, predict fraud, score risk."""
    try:
        logger.info(f"Starting audit orchestration for {file_path}")

        suffix = Path(file_path).suffix.lower()

        # 1. Parse input data
        if suffix == ".csv":
            df = parse_csv(file_path)
        elif suffix in {".xlsx", ".xls"}:
            from .data_service import parse_excel

            df = parse_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

        # 2. Clean data
        df = clean_data(df)

        # 3. Validate transactions
        df, validation_errors = validate_transactions(df)
        if validation_errors:
            logger.warning(f"Validation errors: {validation_errors}")

        # 4. Predict fraud
        df = predict_fraud(df)

        # 5. Score risk
        df = score_risk(df)

        # 6. Generate summary statistics
        summary = {
            "total_records": len(df),
            "high_risk_count": len(df[df["risk_level"] == "High"]),
            "medium_risk_count": len(df[df["risk_level"] == "Medium"]),
            "fraud_detections": len(df[df["anomaly_flag"] == 1]),
            "avg_fraud_score": float(df["fraud_score"].mean()),
            "avg_risk_score": float(df["risk_score"].mean()),
        }

        logger.info(f"Audit completed: {summary}")

        return {
            "status": "success",
            "organization_id": organization_id,
            "summary": summary,
            "data": df.to_dict(orient="records") if len(df) < 1000 else None,
            "validation_errors": validation_errors,
        }
    except Exception as e:
        logger.error(f"Error during audit orchestration: {e}", exc_info=True)
        return {
            "status": "error",
            "message": str(e),
            "organization_id": organization_id
        }
