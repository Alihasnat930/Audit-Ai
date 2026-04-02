"""Fraud detection ML service."""
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def predict_fraud(records: pd.DataFrame) -> pd.DataFrame:
    """Predict fraud probability for transactions using trained ML model.
    
    Returns DataFrame with fraud_score (0-1) and anomaly_flag (0 or 1).
    """
    try:
        from ..ai.fraud_model.model import FraudModel
        from ..ai.fraud_model.utils import preprocess
        from ..config import get_settings
        
        settings = get_settings()
        
        # Load trained model
        model = FraudModel.load(settings.fraud_model_path)
        
        # Preprocess records
        X, _ = preprocess(records)
        
        # Get predictions
        fraud_predictions = model.predict(X)
        fraud_probabilities = model.predict_proba(X)[:, 1]
        
        # Add predictions to records
        records = records.copy()
        records["anomaly_flag"] = fraud_predictions
        records["fraud_score"] = fraud_probabilities
        
        logger.info(f"Fraud detection completed for {len(records)} records")
        return records
    except Exception as e:
        logger.error(f"Error in fraud prediction: {e}")
        return _fallback_fraud_scores(records)


def _fallback_fraud_scores(records: pd.DataFrame) -> pd.DataFrame:
    """Use deterministic heuristics when the ML artifact cannot score the input."""
    df = records.copy()

    amount = _numeric_series(df, "amount")
    vendor_risk = _numeric_series(df, "vendor_risk_score").clip(0, 1)
    duplicate_flag = _numeric_series(df, "duplicate_flag").clip(0, 1)
    missing_invoice_flag = _numeric_series(df, "missing_invoice_flag").clip(0, 1)
    unusual_vendor_flag = _numeric_series(df, "unusual_vendor_flag").clip(0, 1)
    odd_time_flag = _numeric_series(df, "weekend_or_odd_time_flag").clip(0, 1)
    previous_txn_count = _numeric_series(df, "previous_txn_count")

    approval_status = (
        df["approval_status"].fillna("approved").astype(str).str.strip().str.lower()
        if "approval_status" in df
        else pd.Series("approved", index=df.index)
    )

    fraud_score = (
        ((amount >= 5000).astype(float) * 0.08)
        + ((amount >= 10000).astype(float) * 0.16)
        + ((amount >= 20000).astype(float) * 0.18)
        + (vendor_risk * 0.35)
        + (duplicate_flag * 0.22)
        + (missing_invoice_flag * 0.16)
        + (unusual_vendor_flag * 0.20)
        + (odd_time_flag * 0.14)
        + ((previous_txn_count <= 1).astype(float) * 0.08)
        + (approval_status.eq("pending").astype(float) * 0.08)
        + (approval_status.eq("rejected").astype(float) * 0.14)
    ).clip(0, 0.99)

    df["fraud_score"] = fraud_score.round(2)
    df["anomaly_flag"] = (df["fraud_score"] >= 0.65).astype(int)
    logger.info("Fraud fallback scoring completed for %s records", len(df))
    return df


def _numeric_series(df: pd.DataFrame, column: str, default: float = 0.0) -> pd.Series:
    if column in df:
        return pd.to_numeric(df[column], errors="coerce").fillna(default)
    return pd.Series(default, index=df.index, dtype="float64")
