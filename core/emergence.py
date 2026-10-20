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



def local_overlap_profile(
    S1: np.ndarray,
    S2: np.ndarray,
    omega: np.ndarray,
    smoothing_window: int = 31,
) -> np.ndarray:
    """
    Return a peak-normalized local spectral-overlap profile for band finding.

    This is a descriptive, pointwise profile, not the global integrated
    resonance score returned by core.resonance.compute_resonance. The window
    is applied on the supplied sample grid (normally uniform in log-frequency).
    """
    S1 = np.asarray(S1)
    S2 = np.asarray(S2)
    omega = np.asarray(omega, dtype=float)
    if S1.ndim != 1 or S2.ndim != 1 or omega.ndim != 1:
        raise ValueError("S1, S2, and omega must be one-dimensional")
    if not (len(S1) == len(S2) == len(omega)):
        raise ValueError("S1, S2, and omega must have equal lengths")
    if len(omega) == 0:
        return np.array([], dtype=float)
    if len(omega) > 1 and not np.all(np.diff(omega) > 0):
        raise ValueError("omega must be strictly increasing")
    if smoothing_window < 1:
        raise ValueError("smoothing_window must be positive")

    profile = np.abs(S1 * np.conj(S2)).astype(float)
    window = min(int(smoothing_window), len(profile))
    if window > 1:
        if window % 2 == 0:
            window -= 1
        if window > 1:
            kernel = np.ones(window, dtype=float) / window
            profile = np.convolve(profile, kernel, mode="same")
    maximum = float(np.max(profile))
    if maximum > 0 and np.isfinite(maximum):
        profile = profile / maximum
    else:
        profile = np.zeros_like(profile)
    return profile


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
