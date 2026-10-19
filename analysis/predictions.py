"""
Prediction generation from Ω-resonant bands.
"""

from __future__ import annotations

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
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump({"version": "1.0.0", "predictions": predictions}, f, allow_unicode=True, default_flow_style=False)


def list_open_predictions(predictions: List[Dict] | None = None) -> List[Dict]:
    if predictions is None:
        predictions = load_predictions()
    return [p for p in predictions if p.get("status") in ("untested", "undecided")]
