"""
ML anomaly detection engine.
Uses pre-trained Isolation Forest (primary) and DBSCAN (clustering label).
Falls back gracefully if models are not loaded.
"""
import os
import numpy as np
import joblib
from dataclasses import dataclass

MODEL_DIR = os.getenv("MODEL_DIR", "/app/models")

_iso_model = None
_iso_scaler = None
_dbscan_scaler = None


def _load_models():
    global _iso_model, _iso_scaler, _dbscan_scaler
    try:
        _iso_model = joblib.load(f"{MODEL_DIR}/isolation_forest.pkl")
        _iso_scaler = joblib.load(f"{MODEL_DIR}/scaler.pkl")
        _dbscan_scaler = joblib.load(f"{MODEL_DIR}/dbscan_scaler.pkl")
        print("[ML] Models loaded successfully")
    except Exception as e:
        print(f"[ML] Model load warning: {e}")


_load_models()


@dataclass
class MLFeatures:
    requests_per_minute: float
    failed_auth_ratio: float
    unique_endpoints: int
    average_response_time: float
    error_rate: float
    request_interval_variance: float
    sequential_endpoint_patterns: float
    # raw counters for feature vector
    req_count: int = 1
    failed_count: int = 0
    status_404_count: int = 0
    bot_ratio: float = 0.0
    post_ratio: float = 0.0
    login_attempts: int = 0


def build_feature_vector(f: MLFeatures) -> np.ndarray:
    return np.array([[
        f.req_count,
        f.req_count,
        f.req_count,
        f.requests_per_minute / 60.0,
        60.0 / max(f.requests_per_minute, 1),
        f.unique_endpoints,
        f.unique_endpoints,
        f.status_404_count,
        f.error_rate,
        f.bot_ratio,
        f.bot_ratio,
        1.0 - f.bot_ratio,
        f.post_ratio,
        f.req_count,
        f.login_attempts,
        f.failed_count,
        f.failed_auth_ratio,
        f.login_attempts,
        60.0 / max(f.login_attempts, 1),
    ]])


def predict(features: MLFeatures) -> tuple[float, str]:
    """Returns (anomaly_score 0-1, level)."""
    if _iso_model is None or _iso_scaler is None:
        return 0.0, "unknown"
    try:
        vec = build_feature_vector(features)
        scaled = _iso_scaler.transform(vec)
        raw = _iso_model.decision_function(scaled)[0]
        # decision_function: negative = anomaly, positive = normal
        score = float(np.clip(-raw + 0.5, 0.0, 1.0))
        if score >= 0.7:
            level = "CRITICAL"
        elif score >= 0.5:
            level = "HIGH"
        elif score >= 0.3:
            level = "MEDIUM"
        else:
            level = "LOW"
        return round(score, 3), level
    except Exception as e:
        print(f"[ML] Predict error: {e}")
        return 0.0, "unknown"
