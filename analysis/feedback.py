"""
Feedback loop for Omega-RE predictions.

Statuses: untested | confirmed | falsified | undecided
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Any
import copy
import yaml
from datetime import datetime, timezone


PREDICTIONS_PATH = Path(__file__).resolve().parent.parent / "registry" / "predictions.yaml"
RESONANCES_PATH = Path(__file__).resolve().parent.parent / "registry" / "resonances.yaml"
VALID_STATUSES = {"confirmed", "falsified", "undecided", "untested"}


def load_predictions(path: Optional[Path] = None) -> Dict[str, Any]:
    path = PREDICTIONS_PATH if path is None else path
    if not path.exists():
        return {"version": "1.1.0", "predictions": []}
    with open(path, encoding="utf-8") as file:
        return yaml.safe_load(file) or {"version": "1.1.0", "predictions": []}


def save_predictions(data: Dict[str, Any], path: Optional[Path] = None) -> None:
    path = PREDICTIONS_PATH if path is None else path
    data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, allow_unicode=True, default_flow_style=False, sort_keys=False)


def find_prediction(pred_id: str, data: Optional[Dict] = None) -> Optional[Dict]:
    data = load_predictions() if data is None else data
    for prediction in data.get("predictions", []):
        if prediction.get("id") == pred_id:
            return prediction
    return None


def apply_feedback(
    pred_id: str,
    status: str,
    note: str = "",
    dry_run: bool = False,
    evidence_reference: str = "",
) -> Dict[str, Any]:
    """Record workflow feedback without changing model-derived spectral values.

    A confirmed/falsified label requires a reference to supporting evidence.
    The reference is a provenance pointer, not independent verification that
    the evidence or conclusion is scientifically adequate. Dry runs never write.
    """
    status = status.lower().strip()
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    evidence_reference = evidence_reference.strip()
    if status in {"confirmed", "falsified"} and not evidence_reference:
        raise ValueError(
            f"Status '{status}' requires an evidence_reference; "
            "a status label alone is not experimental evidence"
        )

    # Work on a detached copy so a dry run never mutates shared in-memory data.
    data = copy.deepcopy(load_predictions())
    prediction = find_prediction(pred_id, data)
    if prediction is None:
        raise KeyError(f"Prediction {pred_id} not found")

    old_status = prediction.get("status", "untested")
    prediction["status"] = status
    prediction["feedback"] = {
        "previous_status": old_status,
        "note": note,
        "evidence_reference": evidence_reference or None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
    }

    if not dry_run:
        save_predictions(data)
        _update_resonances_log(pred_id, status, note, evidence_reference)
    return prediction


def _update_resonances_log(
    pred_id: str, status: str, note: str, evidence_reference: str = ""
) -> None:
    path = RESONANCES_PATH
    if path.exists():
        with open(path, encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
    else:
        data = {"version": "1.0.0", "entries": []}
    data.setdefault("entries", []).append({
        "prediction_id": pred_id,
        "status": status,
        "note": note,
        "evidence_reference": evidence_reference or None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        yaml.safe_dump(data, file, allow_unicode=True, default_flow_style=False, sort_keys=False)


def list_by_status(status: Optional[str] = None) -> List[Dict]:
    predictions = load_predictions().get("predictions", [])
    if status is None:
        return predictions
    return [prediction for prediction in predictions if prediction.get("status") == status]


def summary() -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for prediction in load_predictions().get("predictions", []):
        status = prediction.get("status", "untested")
        counts[status] = counts.get(status, 0) + 1
    return counts
