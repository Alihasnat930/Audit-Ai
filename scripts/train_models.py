"""Streamlined entrypoint for training both ML models."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "backend"


def run_module(module_name: str) -> None:
    """Run a backend training module inside the backend virtualenv."""
    cmd = [sys.executable, "-m", module_name]
    print(f"Running: {' '.join(cmd)} (cwd={BACKEND_DIR})")
    subprocess.run(cmd, cwd=BACKEND_DIR, check=True)


def main() -> None:
    """Execute both ML training modules."""
    run_module("app.ai.fraud_model.train")
    run_module("app.ai.risk_model.train")


if __name__ == "__main__":
    main()
