"""
Emergent derivation and identification of Ω-resonant bands.

K(T₁ → T₂, Ω) = S_T₂(ω) / S_T₁(ω)
B(T₁, T₂) = { Ω : R_Ω > R_threshold }
"""

from __future__ import annotations

import numpy as np
from typing import List, Dict, Tuple, Optional
from scipy.signal import find_peaks


def compute_kernel(
    S1: np.ndarray,
    S2: np.ndarray,
    eps: float = 1e-10,
) -> np.ndarray:
    """Compute emergent kernel K = S2 / S1 with protection against division by zero."""
    return S2 / (S1 + eps)


def analyze_kernel(
    K: np.ndarray,
    omega: np.ndarray,
    peak_height: float = 0.1,
    zero_threshold: float = 0.01,
) -> Dict:
    """
    Find peaks and zeros of the kernel.

    Returns:
        dict with keys: peaks, zeros, max, min
    """
    abs_K = np.abs(K)
    peaks, _ = find_peaks(abs_K, height=peak_height)
    peak_list = [
        {"omega": float(omega[i]), "value": float(abs_K[i])}
        for i in peaks
    ]
    zero_list = [
        {"omega": float(omega[i]), "value": float(K[i])}
        for i in range(len(K))
        if abs_K[i] < zero_threshold
    ]
    return {
        "peaks": peak_list,
        "zeros": zero_list,
        "max": float(np.max(abs_K)) if len(abs_K) else 0.0,
        "min": float(np.min(abs_K)) if len(abs_K) else 0.0,
    }


def identify_bands(
    omega: np.ndarray,
    R: np.ndarray,
    threshold: float = 0.8,
) -> List[Dict]:
    """
    Identify Ω-resonant bands.

    Returns:
        list of bands with keys: start, end, center, width, max
    """
    bands = []
    in_band = False
    start = None
    max_R = 0.0

    for i, r in enumerate(R):
        if r > threshold and not in_band:
            in_band = True
            start = omega[i]
            max_R = r
        elif r > threshold and in_band:
            max_R = max(max_R, r)
        elif r <= threshold and in_band:
            in_band = False
            end = omega[i - 1] if i > 0 else omega[i]
            if start is not None and end > start:
                bands.append({
                    "start": float(start),
                    "end": float(end),
                    "center": float(np.sqrt(start * end)),
                    "width": float(np.log10(end) - np.log10(start)),
                    "max": float(max_R),
                })
            start = None
            max_R = 0.0

    if in_band and start is not None:
        end = omega[-1]
        bands.append({
            "start": float(start),
            "end": float(end),
            "center": float(np.sqrt(start * end)),
            "width": float(np.log10(end) - np.log10(start)),
            "max": float(max_R),
        })

    return bands


def interpret_band(band: Dict) -> str:
    """Textual interpretation of a band by width and maximum."""
    width = band.get("width", 0)
    rmax = band.get("max", 0)

    if width < 1:
        speed = "sharp transition – rapid emergence"
    elif width <= 3:
        speed = "medium transition – gradual emergence"
    else:
        speed = "broad band – slow emergence or artifact"

    if rmax > 0.95:
        strength = "strong emergence – theories nearly identical"
    elif rmax >= 0.85:
        strength = "medium emergence – theories partially similar"
    else:
        strength = "weak emergence – theories only slightly similar"

    return f"{speed}; {strength}"
