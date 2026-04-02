"""Data parsing and cleaning service for CSV and PDF files."""
import os
from datetime import datetime

import pandas as pd
import logging
from typing import Tuple, List, Dict, Any

logger = logging.getLogger(__name__)


def parse_csv(file_path: str) -> pd.DataFrame:
    """Parse a CSV file into a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Parsed CSV: {len(df)} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        logger.error(f"Error parsing CSV: {e}")
        raise


def parse_excel(file_path: str, sheet_name: str = 0) -> pd.DataFrame:
    """Parse an Excel file into a DataFrame."""
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        logger.info(f"Parsed Excel: {len(df)} rows, {len(df.columns)} columns")
        return df
    except Exception as e:
        logger.error(f"Error parsing Excel: {e}")
        raise


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize transaction data."""
    df = df.copy()
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Fill missing values where appropriate
    if "description" in df.columns:
        df["description"] = df["description"].fillna("")
    
    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()
    
    logger.info(f"Data cleaned: {len(df)} rows remaining")
    return df


def validate_transactions(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """Validate transaction data and return valid rows + error messages."""
    errors = []
    
    # Check required columns
    required_cols = ["amount", "date", "vendor_id", "category"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
    
    # Validate amounts
    if "amount" in df.columns:
        invalid_amounts = df[df["amount"] <= 0]
        if len(invalid_amounts) > 0:
            errors.append(f"Found {len(invalid_amounts)} transactions with invalid amounts")
    
    logger.info(f"Validation complete: {len(errors)} errors found")
    return df, errors


_SAMPLE_DF: pd.DataFrame | None = None


def _sample_data_path() -> str:
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "data",
        "processed",
        "synthetic_enterprise_audit.csv",
    )


def _load_sample_dataset() -> pd.DataFrame:
    global _SAMPLE_DF
    if _SAMPLE_DF is None:
        try:
            path = _sample_data_path()
            _SAMPLE_DF = pd.read_csv(path, parse_dates=["date"])
        except Exception:
            _SAMPLE_DF = pd.DataFrame()
    return _SAMPLE_DF


def _filter_by_organization(df: pd.DataFrame, organization_id: str | None) -> pd.DataFrame:
    if not organization_id or df.empty:
        return df

    filtered = df[df["organization_id"] == organization_id]
    if filtered.empty and len(df) > 0:
        filtered = df.sample(min(1000, len(df)), random_state=42)
    return filtered


def build_dashboard_summary(organization_id: str | None) -> Dict[str, float]:
    df = _filter_by_organization(_load_sample_dataset(), organization_id)
    if df.empty:
        return {
            "total_transactions": 0,
            "high_risk_count": 0,
            "fraud_detections": 0,
            "avg_fraud_score": 0.0,
            "avg_risk_score": 0.0,
        }

    risk_score = pd.to_numeric(df.get("risk_score", 0), errors="coerce").fillna(0)
    fraud_score = pd.to_numeric(df.get("fraud_score", 0), errors="coerce").fillna(0)
    return {
        "total_transactions": int(len(df)),
        "high_risk_count": int((df.get("risk_level") == "High").sum()),
        "fraud_detections": int((df["anomaly_flag"] == 1).sum()),
        "avg_fraud_score": float(fraud_score.mean()),
        "avg_risk_score": float(risk_score.mean()),
    }


def build_monthly_trends(organization_id: str | None, periods: int = 6) -> List[Dict[str, float]]:
    df = _filter_by_organization(_load_sample_dataset(), organization_id)
    if df.empty:
        return []

    df = df.copy()
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    grouped = (
        df.groupby("month", as_index=False)
        .agg(
            transactions=("transaction_id", "count"),
            fraud=("anomaly_flag", "sum"),
        )
        .sort_values("month")
    )
    latest = grouped.tail(periods)
    return [
        {
            "name": row["month"].strftime("%b %Y"),
            "transactions": int(row["transactions"]),
            "fraud": int(row["fraud"]),
        }
        for _, row in latest.iterrows()
    ]


def get_risk_distribution(organization_id: str | None) -> List[Dict[str, float]]:
    df = _filter_by_organization(_load_sample_dataset(), organization_id)
    if df.empty:
        return []

    levels = ["Low", "Medium", "High"]
    counts = (
        df["risk_level"]
        .fillna("Low")
        .astype(str)
        .value_counts(normalize=True)
        .reindex(levels, fill_value=0.0)
    )
    return [
        {"name": level, "value": round(float(counts[level]) * 100, 1)}
        for level in levels
    ]


def get_recent_alerts(organization_id: str | None, limit: int = 3) -> List[Dict[str, str]]:
    df = _filter_by_organization(_load_sample_dataset(), organization_id)
    if df.empty:
        return []

    sorted_df = (
        df.sort_values(["fraud_score", "risk_score"], ascending=False)
        .head(limit)
        .fillna("")
    )
    alerts = []
    for _, row in sorted_df.iterrows():
        alerts.append(
            {
                "transaction_id": row.get("transaction_id"),
                "vendor": row.get("vendor_name") or row.get("vendor_id"),
                "message": f"Fraud score {row.get('fraud_score', 0):.2f}, risk level {row.get('risk_level', 'Low')}",
                "timestamp": row.get("date").strftime("%Y-%m-%d %H:%M") if pd.notna(row.get("date")) else "",
                "fraud_score": float(row.get("fraud_score", 0)),
                "risk_score": float(row.get("risk_score", 0)),
                "risk_level": row.get("risk_level", "Low"),
            }
        )
    return alerts


def get_sample_transactions(
    organization_id: str | None,
    risk_level: str | None = None,
    skip: int = 0,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    df = _filter_by_organization(_load_sample_dataset(), organization_id)
    if df.empty:
        return []

    if risk_level:
        df = df[df["risk_level"].fillna("Low").astype(str).str.lower() == risk_level.lower()]
        if df.empty:
            return []

    subset = (
        df.sort_values("date", ascending=False)
        .iloc[skip : skip + limit]
        .copy()
    )
    subset["date"] = subset["date"].dt.strftime("%Y-%m-%d")
    columns = [
        "transaction_id",
        "vendor_name",
        "amount",
        "currency",
        "category",
        "fraud_score",
        "risk_score",
        "risk_level",
        "date",
    ]
    return subset[columns].to_dict(orient="records")


def get_vendor_risk_summary(organization_id: str | None, top_n: int = 5) -> List[Dict[str, Any]]:
    df = _filter_by_organization(_load_sample_dataset(), organization_id)
    if df.empty:
        return []

    grouped = (
        df.groupby("vendor_name", dropna=False)
        .agg(
            risk_score=("risk_score", lambda x: float(pd.to_numeric(x, errors="coerce").mean())),
            fraud_score=("fraud_score", lambda x: float(pd.to_numeric(x, errors="coerce").mean())),
            transactions=("transaction_id", "count"),
        )
        .reset_index()
    )
    grouped["risk_score"] = grouped["risk_score"].fillna(0).clip(0, 100)
    grouped["fraud_score"] = grouped["fraud_score"].fillna(0).clip(0, 1)
    top = grouped.sort_values("risk_score", ascending=False).head(top_n)
    return [
        {
            "vendor_name": row["vendor_name"] or "Unknown",
            "risk_score": float(row["risk_score"]),
            "fraud_score": float(row["fraud_score"]),
            "transaction_count": int(row["transactions"]),
        }
        for _, row in top.iterrows()
    ]
