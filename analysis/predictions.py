"""
Prediction generation from Ω-resonant bands.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Any
import yaml
from pathlib import Path


def generate_prediction(
    t1: str,
    t2: str,
    band: Dict[str, float],
    deviation_symbol: str = "Δ",
    measurement: str = "to be specified",
) -> Dict[str, Any]:
    """Create a prediction record for a resonant band."""
    return {
        "T1": t1,
        "T2": t2,
        "band": band,
        "deviation": {
            "symbol": deviation_symbol,
            "value": None,
            "unit": "dimensionless",
        },
        "measurement": measurement,
        "falsification": f"No deviation observed inside band [{band.get('start')}, {band.get('end')}]",
        "status": "untested",
    }


def load_predictions(path: Path = Path("registry/predictions.yaml")) -> List[Dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("predictions", [])


def save_predictions(predictions: List[Dict], path: Path = Path("registry/predictions.yaml")) -> None:
    """Save prediction records while retaining existing registry-level metadata."""
    data: Dict[str, Any] = {}
    if path.exists():
        with open(path, encoding="utf-8") as f:
            loaded = yaml.safe_load(f) or {}
        if isinstance(loaded, dict):
            data = loaded.copy()

    data.setdefault("version", "1.0.0")
    data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    data["predictions"] = predictions

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def list_open_predictions(predictions: List[Dict] | None = None) -> List[Dict]:
    if predictions is None:
        predictions = load_predictions()
    return [p for p in predictions if p.get("status") in ("untested", "undecided")]
