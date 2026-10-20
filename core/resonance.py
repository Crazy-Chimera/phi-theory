"""
Computation of Omega-resonance between theories.

R = |integral S1(omega) * conjugate(S2(omega)) d omega|^2
    / (integral |S1|^2 d omega * integral |S2|^2 d omega)
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import trapezoid
from typing import Dict, Tuple, Optional


def _validate_grid(omega: np.ndarray) -> None:
    if omega.ndim != 1:
        raise ValueError("omega must be a one-dimensional array")
    if not np.all(np.isfinite(omega)):
        raise ValueError("omega values must be finite")
    if len(omega) > 1 and not np.all(np.diff(omega) > 0):
        raise ValueError("omega must be strictly increasing")


def compute_resonance(
    S1: np.ndarray,
    S2: np.ndarray,
    omega: np.ndarray,
) -> float:
    """Compute normalized spectral overlap using the actual grid coordinates."""
    S1 = np.asarray(S1)
    S2 = np.asarray(S2)
    omega = np.asarray(omega, dtype=float)
    if S1.ndim != 1 or S2.ndim != 1 or omega.ndim != 1:
        raise ValueError("S1, S2, and omega must be one-dimensional")
    if not (len(S1) == len(S2) == len(omega)):
        raise ValueError("S1, S2, and omega must have equal lengths")
    if not np.all(np.isfinite(S1)) or not np.all(np.isfinite(S2)):
        raise ValueError("S1 and S2 values must be finite")
    _validate_grid(omega)
    if len(omega) < 2:
        return 0.0

    # Extreme but finite inputs can overflow during products or quadrature.
    # Treat an unrepresentable overlap as undefined (score 0) rather than
    # allowing NaN to escape through np.clip.
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        cross = trapezoid(S1 * np.conj(S2), x=omega)
        norm1 = float(trapezoid(np.abs(S1) ** 2, x=omega))
        norm2 = float(trapezoid(np.abs(S2) ** 2, x=omega))
        norm_product = norm1 * norm2
        numerator = np.abs(cross) ** 2
    if (
        norm1 <= 0 or norm2 <= 0
        or not np.isfinite(norm1)
        or not np.isfinite(norm2)
        or not np.isfinite(norm_product)
        or not np.isfinite(cross)
        or not np.isfinite(numerator)
    ):
        return 0.0
    value = float(numerator / norm_product)
    if not np.isfinite(value):
        return 0.0
    # Numerical quadrature can produce tiny excursions outside the theoretical range.
    return float(np.clip(value, 0.0, 1.0))


def interpolate_to_grid(
    omega_src: np.ndarray,
    S_src: np.ndarray,
    omega_target: np.ndarray,
) -> np.ndarray:
    """Interpolate a spectrum onto a positive, logarithmic-frequency target grid."""
    omega_src = np.asarray(omega_src, dtype=float)
    omega_target = np.asarray(omega_target, dtype=float)
    S_src = np.asarray(S_src)
    if omega_src.ndim != 1 or omega_target.ndim != 1 or S_src.ndim != 1:
        raise ValueError("omega_src, S_src, and omega_target must be one-dimensional")
    if len(omega_src) != len(S_src) or len(omega_src) == 0:
        raise ValueError("omega_src and S_src must have equal non-zero lengths")
    _validate_grid(omega_src)
    _validate_grid(omega_target)
    if not np.all(np.isfinite(S_src)):
        raise ValueError("S_src values must be finite")
    if np.any(omega_src <= 0) or np.any(omega_target <= 0):
        raise ValueError("log-scale interpolation requires positive frequencies")
    log_src = np.log10(omega_src)
    log_tgt = np.log10(omega_target)
    real = np.interp(log_tgt, log_src, np.real(S_src), left=0.0, right=0.0)
    imag = np.interp(log_tgt, log_src, np.imag(S_src), left=0.0, right=0.0)
    return real + 1j * imag


def resonance_matrix(
    spectra: Dict[str, Tuple[np.ndarray, np.ndarray]],
    omega_grid: Optional[np.ndarray] = None,
    n_samples: int = 10_000,
) -> Dict[str, Dict[str, float]]:
    """Compute the symmetric resonance matrix for a mapping of named spectra."""
    if omega_grid is None:
        omega_grid = np.logspace(-10, 10, n_samples)
    else:
        omega_grid = np.asarray(omega_grid, dtype=float)
        _validate_grid(omega_grid)

    names = list(spectra.keys())
    matrix: Dict[str, Dict[str, float]] = {name: {} for name in names}
    interp = {
        name: interpolate_to_grid(omega, spectrum, omega_grid)
        for name, (omega, spectrum) in spectra.items()
    }

    for i, t1 in enumerate(names):
        for t2 in names[i:]:
            value = compute_resonance(interp[t1], interp[t2], omega_grid)
            matrix[t1][t2] = value
            matrix[t2][t1] = value
    return matrix


def qualitative_resonance(
    range1: Tuple[float, float],
    range2: Tuple[float, float],
    shape_similar: bool = True,
) -> float:
    """Return a heuristic range-overlap score; this is not measured resonance."""
    if min(*range1, *range2) <= 0 or range1[1] <= range1[0] or range2[1] <= range2[0]:
        raise ValueError("ranges must be positive and increasing")
    low = max(range1[0], range2[0])
    high = min(range1[1], range2[1])
    if high <= low:
        return 0.1
    overlap = np.log10(high) - np.log10(low)
    width1 = np.log10(range1[1]) - np.log10(range1[0])
    width2 = np.log10(range2[1]) - np.log10(range2[0])
    fraction = overlap / max(width1, width2, 1e-12)
    if fraction > 0.8 and shape_similar:
        return 0.9
    if fraction > 0.5:
        return 0.7
    if fraction > 0.2:
        return 0.4
    return 0.1
