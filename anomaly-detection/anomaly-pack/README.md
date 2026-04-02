# Anomaly Package — AuditAI

This folder contains the minimal set of files required to reproduce the anomaly detection model and experiments from the AuditAI project.

Contents
- `notebooks/`
  - `model_experiments.ipynb` — EDA, feature engineering, training and evaluation notebook.
  - `train_models.py` — Runnable training script (same workflow as the notebook).
  - `datagen.py` — Synthetic data generation helper.
  - `requirements.txt` — Python dependencies used for the notebook/training.
- `fraud_model/`
  - `model.py` — Lightweight wrapper for the trained classifier.
  - `train.py` — training helper used by the backend.
  - `utils.py` — preprocessing/utilities.
  - `artifacts/`
    - `fraud_classifier.joblib` — trained RandomForest classifier (binary).
    - `fraud_metrics.json` — evaluation metrics for the model.
- `data/`
  - `synthetic_enterprise_audit.csv` — synthetic example dataset used in experiments.

Quickstart
1. Create a Python virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate   # or `venv\Scripts\Activate.ps1` on Windows
pip install -r notebooks/requirements.txt
```

2. Open `notebooks/model_experiments.ipynb` and run cells to reproduce EDA and training, or run the training script:

```bash
python notebooks/train_models.py
```

3. Load the trained model from Python:

```python
from fraud_model.model import FraudModel
m = FraudModel.load('fraud_model/artifacts/fraud_classifier.joblib')
# prepare a DataFrame `X` using the notebook's build_feature_matrix
preds = m.predict_proba(X)[:,1]
```

Notes
- The dataset is synthetic and included for demonstration and presentations.
- `fraud_classifier.joblib` is a binary model artifact (~2MB). If you prefer not to store datasets or artifacts in the repo, consider using Git LFS.

License and attribution
- Files copied from AuditAI project for the purpose of sharing the anomaly model and experiments.

