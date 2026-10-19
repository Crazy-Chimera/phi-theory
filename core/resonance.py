"""
Computation of Ω-resonance between theories.

R_Ω(T₁, T₂) = |∫ S_T₁(ω) · S_T₂*(ω) dω|² / (∫|S_T₁|² dω · ∫|S_T₂|² dω)
"""

from __future__ import annotations

import numpy as np
from typing import List, Dict, Tuple, Optional


def compute_resonance(
    S1: np.ndarray,
    S2: np.ndarray,
    omega: np.ndarray,
) -> float:
    """
    Compute normalized cross-correlation (Ω-resonance).

    Returns:
        R_Ω ∈ [0, 1]
    """
    if len(omega) < 2:
        return 0.0
    dω = omega[1] - omega[0]
    C = np.sum(S1 * np.conj(S2)) * dω
    N1 = np.sum(np.abs(S1) ** 2) * dω
    N2 = np.sum(np.abs(S2) ** 2) * dω
    if N1 == 0 or N2 == 0:
        return 0.0
    return float(np.abs(C) ** 2 / (N1 * N2))


def interpolate_to_grid(
    omega_src: np.ndarray,
    S_src: np.ndarray,
    omega_target: np.ndarray,
) -> np.ndarray:
    """Interpolate spectrum onto a target grid (log-scale friendly)."""
    log_src = np.log10(np.clip(omega_src, 1e-30, None))
    log_tgt = np.log10(np.clip(omega_target, 1e-30, None))
    real = np.interp(log_tgt, log_src, np.real(S_src), left=0.0, right=0.0)
    imag = np.interp(log_tgt, log_src, np.imag(S_src), left=0.0, right=0.0)
    return real + 1j * imag


def resonance_matrix(
    spectra: Dict[str, Tuple[np.ndarray, np.ndarray]],
    omega_grid: Optional[np.ndarray] = None,
    n_samples: int = 10_000,
) -> Dict[str, Dict[str, float]]:
    """
    Compute the R_Ω matrix for all pairs of theories.

    Args:
        spectra: {name: (omega, S)}
        omega_grid: common grid (if None, creates logspace)
        n_samples: number of grid points

    Returns:
        nested dict R[T1][T2] = R_Ω
    """
    if omega_grid is None:
        omega_grid = np.logspace(-10, 10, n_samples)

    names = list(spectra.keys())
    matrix: Dict[str, Dict[str, float]] = {n: {} for n in names}

    interp: Dict[str, np.ndarray] = {}
    for name, (ω, S) in spectra.items():
        interp[name] = interpolate_to_grid(ω, S, omega_grid)

    for i, t1 in enumerate(names):
        for t2 in names[i:]:
            R = compute_resonance(interp[t1], interp[t2], omega_grid)
            matrix[t1][t2] = R
            matrix[t2][t1] = R  # symmetry

    return matrix


def qualitative_resonance(
    range1: Tuple[float, float],
    range2: Tuple[float, float],
    shape_similar: bool = True,
) -> float:
    """
    Qualitative resonance estimate from Ω-range overlap.
    """
    low = max(range1[0], range2[0])
    high = min(range1[1], range2[1])
    if high <= low:
        return 0.1
    overlap = np.log10(high) - np.log10(low)
    width1 = np.log10(range1[1]) - np.log10(range1[0])
    width2 = np.log10(range2[1]) - np.log10(range2[0])
    frac = overlap / max(width1, width2, 1e-12)
    if frac > 0.8 and shape_similar:
        return 0.9
    if frac > 0.5:
        return 0.7
    if frac > 0.2:
        return 0.4
    return 0.1
