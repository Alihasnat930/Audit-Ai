import pandas as pd


def apply_risk_rules(records: pd.DataFrame) -> pd.DataFrame:
    """Apply deterministic rules to seed a risk score before ML refinement."""
    df = records.copy()
    df["risk_score"] = _numeric_series(df, "risk_score")
    df["fraud_score"] = _numeric_series(df, "fraud_score").clip(0, 1)
    df["vendor_risk_score"] = _numeric_series(df, "vendor_risk_score").clip(0, 1)

    amount = _numeric_series(df, "amount")
    df["risk_score"] += _amount_risk(amount)
    df["risk_score"] += df["vendor_risk_score"] * 20
    df["risk_score"] += df["fraud_score"] * 40

    flag_weights = {
        "duplicate_flag": 5,
        "missing_invoice_flag": 15,
        "unusual_vendor_flag": 10,
        "weekend_or_odd_time_flag": 8,
    }
    for flag, weight in flag_weights.items():
        df["risk_score"] += _numeric_series(df, flag) * weight

    df["risk_score"] = df["risk_score"].clip(0, 100)
    return df


def _amount_risk(amount: pd.Series) -> pd.Series:
    """Translate transaction amount into a risk bump."""
    bins = [0, 1000, 5000, 10000, 25000, float("inf")]
    weights = [2, 8, 15, 25, 35]
    risk = pd.cut(amount, bins=bins, labels=weights, right=False)
    return risk.astype(float).fillna(0)


def _numeric_series(df: pd.DataFrame, column: str, default: float = 0.0) -> pd.Series:
    if column in df:
        return pd.to_numeric(df[column], errors="coerce").fillna(default)
    return pd.Series(default, index=df.index, dtype="float64")
