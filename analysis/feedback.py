"""
Feedback loop for Ω-RE predictions.

Statuses: untested | confirmed | falsified | undecided
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
from datetime import datetime, timezone


PREDICTIONS_PATH = Path(__file__).resolve().parent.parent / "registry" / "predictions.yaml"
RESONANCES_PATH = Path(__file__).resolve().parent.parent / "registry" / "resonances.yaml"


def load_predictions(path: Path = PREDICTIONS_PATH) -> Dict[str, Any]:
    if not path.exists():
        return {"version": "1.1.0", "predictions": []}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {"version": "1.1.0", "predictions": []}


def save_predictions(data: Dict[str, Any], path: Path = PREDICTIONS_PATH) -> None:
    data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def find_prediction(pred_id: str, data: Optional[Dict] = None) -> Optional[Dict]:
    data = data or load_predictions()
    for p in data.get("predictions", []):
        if p.get("id") == pred_id:
            return p
    return None


def apply_feedback(
    pred_id: str,
    status: str,
    note: str = "",
    strengthen: float = 0.05,
    weaken: float = 0.05,
) -> Dict[str, Any]:
    status = status.lower().strip()
    if status not in ("confirmed", "falsified", "undecided", "untested"):
        raise ValueError(f"Invalid status: {status}")

    data = load_predictions()
    pred = find_prediction(pred_id, data)
    if not pred:
        raise KeyError(f"Prediction {pred_id} not found")

    old = pred.get("status", "untested")
    pred["status"] = status
    pred["feedback"] = {
        "previous_status": old,
        "note": note,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    band = pred.get("band")
    if band is not None:
        strength = float(band.get("strength", band.get("max", 1.0)))
        if status == "confirmed":
            strength = min(1.0, strength + strengthen)
            band["strength"] = strength
            band["feedback_effect"] = "strengthened"
        elif status == "falsified":
            strength = max(0.0, strength - weaken)
            band["strength"] = strength
            band["feedback_effect"] = "weakened"
        else:
            band["feedback_effect"] = "unchanged"

    save_predictions(data)
    _update_resonances_log(pred_id, status, note)
    return pred


def _update_resonances_log(pred_id: str, status: str, note: str) -> None:
    path = RESONANCES_PATH
    if path.exists():
        with open(path, encoding="utf-8") as f:
            res = yaml.safe_load(f) or {}
    else:
        res = {"version": "1.0.0", "entries": []}
    entries = res.setdefault("entries", [])
    entries.append({
        "prediction_id": pred_id,
        "status": status,
        "note": note,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    res["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(res, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def list_by_status(status: Optional[str] = None) -> List[Dict]:
    data = load_predictions()
    preds = data.get("predictions", [])
    if status is None:
        return preds
    return [p for p in preds if p.get("status") == status]


def summary() -> Dict[str, int]:
    data = load_predictions()
    counts: Dict[str, int] = {}
    for p in data.get("predictions", []):
        s = p.get("status", "untested")
        counts[s] = counts.get(s, 0) + 1
    return counts
