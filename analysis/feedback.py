"""
Feedback loop for Omega-RE predictions.

Statuses: untested | confirmed | falsified | undecided
"""

from __future__ import annotations

from pathlib import Path
import os
import tempfile
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
    if not isinstance(status, str):
        raise ValueError("status must be a string")
    status = status.lower().strip()
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    if not isinstance(evidence_reference, str):
        raise ValueError("evidence_reference must be a string")
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
        # Parse and validate the second file before writing the first, so a
        # malformed log cannot leave the registry updated on its own.
        resonance_data = _load_resonances_log(RESONANCES_PATH)
        _append_resonance_entry(
            resonance_data, pred_id, status, note, evidence_reference
        )
        _persist_feedback_pair(data, resonance_data)
    return prediction


def _load_resonances_log(path: Path) -> Dict[str, Any]:
    """Load and validate the resonance log before any paired registry write."""
    if path.exists():
        with open(path, encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
    else:
        data = {"version": "1.0.0", "entries": []}
    if not isinstance(data, dict):
        raise ValueError("resonance log must contain a YAML mapping")
    entries = data.setdefault("entries", [])
    if not isinstance(entries, list):
        raise ValueError("resonance log 'entries' must be a YAML list")
    return data


def _append_resonance_entry(
    data: Dict[str, Any],
    pred_id: str,
    status: str,
    note: str,
    evidence_reference: str = "",
) -> None:
    data["entries"].append({
        "prediction_id": pred_id,
        "status": status,
        "note": note,
        "evidence_reference": evidence_reference or None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    data["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _stage_bytes(path: Path, payload: bytes) -> Path:
    """Write and fsync a temporary file beside its destination."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as file:
            file.write(payload)
            file.flush()
            os.fsync(file.fileno())
    except BaseException:
        temp_path.unlink(missing_ok=True)
        raise
    return temp_path


def _atomic_write_bytes(path: Path, payload: bytes) -> None:
    temp_path = _stage_bytes(path, payload)
    try:
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)


def _persist_feedback_pair(
    predictions: Dict[str, Any], resonances: Dict[str, Any]
) -> None:
    """Stage both YAML files and roll back the first replacement if the second fails.

    This narrows ordinary partial-write failures, but cannot guarantee recovery
    from process termination or power loss between the two replacements.
    """
    prediction_path = PREDICTIONS_PATH
    resonance_path = RESONANCES_PATH
    prediction_payload = yaml.safe_dump(
        predictions, allow_unicode=True, default_flow_style=False, sort_keys=False
    ).encode("utf-8")
    resonance_payload = yaml.safe_dump(
        resonances, allow_unicode=True, default_flow_style=False, sort_keys=False
    ).encode("utf-8")

    original_prediction = prediction_path.read_bytes() if prediction_path.exists() else None
    staged_prediction = _stage_bytes(prediction_path, prediction_payload)
    try:
        staged_resonance = _stage_bytes(resonance_path, resonance_payload)
    except BaseException:
        staged_prediction.unlink(missing_ok=True)
        raise

    prediction_replaced = False
    try:
        os.replace(staged_prediction, prediction_path)
        prediction_replaced = True
        os.replace(staged_resonance, resonance_path)
    except BaseException:
        if prediction_replaced:
            try:
                if original_prediction is None:
                    prediction_path.unlink(missing_ok=True)
                else:
                    _atomic_write_bytes(prediction_path, original_prediction)
            except BaseException as rollback_error:
                raise RuntimeError(
                    "feedback persistence failed and prediction-registry rollback also failed"
                ) from rollback_error
        raise
    finally:
        staged_prediction.unlink(missing_ok=True)
        staged_resonance.unlink(missing_ok=True)


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
