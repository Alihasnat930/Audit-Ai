"""Train and persist the risk regression model."""
import json
import os

import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

try:
    from .scoring import build_feature_matrix, persist_feature_columns
except ImportError:  # pragma: no cover
    from app.ai.risk_model.scoring import build_feature_matrix, persist_feature_columns


ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
MODEL_PATH = os.path.join(ARTIFACT_DIR, "risk_regressor.joblib")
METRICS_PATH = os.path.join(ARTIFACT_DIR, "risk_metrics.json")


def _default_data_path():
    root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )
    return os.path.join(root, "data", "processed", "synthetic_enterprise_audit.csv")


def train_risk_model(data_path=None, random_state=42):
    data_path = data_path or _default_data_path()
    df = pd.read_csv(data_path)
    y = pd.to_numeric(df.get("risk_score", 0), errors="coerce").fillna(0)

    X = build_feature_matrix(df)
    feature_columns = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )

    model = HistGradientBoostingRegressor(
        max_iter=200,
        random_state=random_state,
        learning_rate=0.05,
        max_depth=8,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    metrics = {
        "mae": float(mean_absolute_error(y_test, preds)),
        "r2": float(r2_score(y_test, preds)),
    }

    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    persist_feature_columns(feature_columns)
    with open(METRICS_PATH, "w", encoding="utf-8") as fp:
        json.dump(metrics, fp, indent=2)

    print("Risk model trained:", MODEL_PATH)
    print("Metrics:", metrics)
    return MODEL_PATH, metrics


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train the risk scoring regressor")
    parser.add_argument("--data", type=str, help="Path to CSV file")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    train_risk_model(data_path=args.data, random_state=args.seed)
