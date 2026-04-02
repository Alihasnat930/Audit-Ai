import json
import os

import joblib
import numpy as np
import pandas as pd


DEFAULT_ARTIFACT = os.path.join(os.path.dirname(__file__), "artifacts", "risk_regressor.joblib")


class RiskModel:
    def __init__(self, model, feature_columns=None):
        self.model = model
        self.feature_columns = feature_columns or []

    @classmethod
    def load(cls, path=None):
        path = path or DEFAULT_ARTIFACT
        model = joblib.load(path)
        feature_columns = []
        spec_path = os.path.join(os.path.dirname(path), "risk_feature_columns.json")
        if os.path.exists(spec_path):
            with open(spec_path, "r", encoding="utf-8") as fp:
                feature_columns = json.load(fp)
        return cls(model, feature_columns)

    def predict(self, X):
        arr = self._ensure_array(X)
        preds = self.model.predict(arr)
        return np.clip(preds, 0, 100)

    def _ensure_array(self, X):
        if isinstance(X, pd.DataFrame):
            return X.values
        if isinstance(X, (list, tuple, np.ndarray)):
            return np.array(X)
        raise ValueError("RiskModel expects a numeric matrix or pandas DataFrame.")
