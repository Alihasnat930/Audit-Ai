"""Risk scoring ML service and rule-based risk assessment."""
import logging

import pandas as pd

from ..config import get_settings
from ..ai.risk_model.model import RiskModel
from ..ai.risk_model.rules import apply_risk_rules
from ..ai.risk_model.scoring import build_feature_matrix, load_feature_columns

logger = logging.getLogger(__name__)
settings = get_settings()


def score_risk(records: pd.DataFrame) -> pd.DataFrame:
    """Assign risk scores (0-100) and risk levels (Low, Medium, High)."""
    df = records.copy()
    try:
        df = apply_risk_rules(df)
        ml_scores = _predict_ml_risk(df)
        if ml_scores is not None:
            df["risk_score"] = (df["risk_score"] * 0.4 + ml_scores * 0.6).clip(0, 100)
        else:
            df["risk_score"] = df["risk_score"].clip(0, 100)
        df["risk_level"] = _map_risk_level(df["risk_score"])
        logger.info(f"Risk scoring completed for {len(df)} records")
    except Exception as exc:
        logger.error(f"Error in risk scoring: {exc}")
        df["risk_score"] = 0.0
        df["risk_level"] = "Low"
    return df


def _predict_ml_risk(df: pd.DataFrame) -> pd.Series | None:
    """Use the trained regressor to refine the rule-based score."""
    try:
        risk_model = RiskModel.load(settings.risk_model_path)
        feature_columns = risk_model.feature_columns or load_feature_columns()
        if not feature_columns:
            return None
        feature_matrix = build_feature_matrix(df, feature_columns=feature_columns)
        return pd.Series(risk_model.predict(feature_matrix), index=df.index)
    except Exception as exc:
        logger.warning(f"ML risk model unavailable: {exc}")
        return None


def _map_risk_level(scores: pd.Series) -> pd.Series:
    categories = pd.cut(
        scores,
        bins=[-0.1, 30, 70, 100],
        labels=["Low", "Medium", "High"],
        include_lowest=True,
    )
    return categories.astype(str).replace("nan", "Low")
