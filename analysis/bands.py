"""
Identification of Ω-resonant bands from resonance data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict

import numpy as np

from core.emergence import identify_bands


def load_resonance_curve(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Load R(Ω) curve from JSON."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    omega = np.array(data["omega"])
    R = np.array(data["R_omega"])
    return omega, R


def process_pair(
    omega: np.ndarray,
    R: np.ndarray,
    threshold: float = 0.8,
) -> List[Dict]:
    return identify_bands(omega, R, threshold=threshold)


def save_bands(bands: List[Dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"bands": bands}, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Identify Ω-bands")
    parser.add_argument("--input", default="data/resonance_curve.json")
    parser.add_argument("--output", default="registry/bands.json")
    parser.add_argument("--threshold", type=float, default=0.8)
    args = parser.parse_args()

    omega, R = load_resonance_curve(Path(args.input))
    bands = process_pair(omega, R, threshold=args.threshold)
    save_bands(bands, Path(args.output))
    print(f"Found {len(bands)} bands → {args.output}")
