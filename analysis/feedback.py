"""
Feedback loop for Ω-RE: update resonance strength from experimental outcomes.
"""

from __future__ import annotations

from typing import Dict, List, Literal
import yaml
from pathlib import Path

Outcome = Literal["confirmed", "falsified", "undecided"]


def apply_feedback(
    resonances: List[Dict],
    prediction_id: str,
    outcome: Outcome,
    strength_delta: float = 0.05,
) -> List[Dict]:
    """
    Strengthen or weaken the resonant band associated with a prediction.
    """
    for r in resonances:
        if outcome == "confirmed":
            r["R_omega"] = min(1.0, r.get("R_omega", 0.8) + strength_delta)
        elif outcome == "falsified":
            r["R_omega"] = max(0.0, r.get("R_omega", 0.8) - strength_delta)
    return resonances


def load_resonances(path: Path = Path("registry/resonances.yaml")) -> List[Dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("resonances", [])


def save_resonances(resonances: List[Dict], path: Path = Path("registry/resonances.yaml")) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(
            {"version": "1.0.0", "threshold": 0.8, "resonances": resonances},
            f,
            allow_unicode=True,
            default_flow_style=False,
        )
