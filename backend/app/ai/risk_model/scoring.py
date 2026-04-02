import json
import os
from typing import List, Optional

import pandas as pd


BASE_DIR = os.path.dirname(__file__)
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")
FEATURE_SPEC_PATH = os.path.join(ARTIFACT_DIR, "risk_feature_columns.json")

NUMERIC_FEATURES = [
    "amount",
    "tax_amount",
    "vendor_risk_score",
    "fraud_score",
    "duplicate_flag",
    "missing_invoice_flag",
    "unusual_vendor_flag",
    "weekend_or_odd_time_flag",
    "user_tenure_days",
    "previous_txn_count",
]
CATEGORICAL_FEATURES = ["category", "payment_method", "approval_status"]


def build_feature_matrix(df: pd.DataFrame, feature_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Build a feature DataFrame for training/inference."""
    df = df.copy()
    for col in NUMERIC_FEATURES:
        df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)

    dummies = []
    for col in CATEGORICAL_FEATURES:
        if col in df:
            cat = df[col].fillna("unknown").astype(str)
        else:
            cat = pd.Series("unknown", index=df.index)
        dummies.append(pd.get_dummies(cat, prefix=col, prefix_sep="_"))

    frames = [df[NUMERIC_FEATURES]] + dummies
    X = pd.concat(frames, axis=1, copy=False).fillna(0)

    if feature_columns:
        for column in feature_columns:
            if column not in X.columns:
                X[column] = 0
        extra = [column for column in X.columns if column not in feature_columns]
        if extra:
            X = X.drop(columns=extra)
        X = X[feature_columns]

    return X


def persist_feature_columns(columns: List[str]) -> None:
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    with open(FEATURE_SPEC_PATH, "w", encoding="utf-8") as fp:
        json.dump(columns, fp, indent=2)


def load_feature_columns() -> List[str]:
    if os.path.exists(FEATURE_SPEC_PATH):
        with open(FEATURE_SPEC_PATH, "r", encoding="utf-8") as fp:
            return json.load(fp)
    return []
