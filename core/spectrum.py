"""
Spectral decomposition of theories (Omega-spectrum).

T(Omega) = integral S_T(omega) * exp(i * omega * Omega) d omega
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import trapezoid
from typing import Tuple, Optional, Dict, Any


def _validate_grid(omega: np.ndarray) -> None:
    """Require a one-dimensional, strictly increasing integration grid."""
    if omega.ndim != 1:
        raise ValueError("omega must be a one-dimensional array")
    if not np.all(np.isfinite(omega)):
        raise ValueError("omega values must be finite")
    if len(omega) > 1 and not np.all(np.diff(omega) > 0):
        raise ValueError("omega must be strictly increasing")


def normalize_spectrum(S: np.ndarray, omega: np.ndarray) -> np.ndarray:
    """Normalize S so that the trapezoidal approximation to integral |S|^2 dω is 1."""
    S = np.asarray(S)
    omega = np.asarray(omega, dtype=float)
    if S.ndim != 1 or omega.ndim != 1 or len(S) != len(omega):
        raise ValueError("S and omega must be one-dimensional arrays of equal length")
    if len(omega) < 2:
        return S.copy()
    _validate_grid(omega)
    norm_sq = float(trapezoid(np.abs(S) ** 2, x=omega))
    if not np.isfinite(norm_sq) or norm_sq <= 0:
        return S.copy()
    return S / np.sqrt(norm_sq)


def compute_spectrum_explicit(
    H: np.ndarray,
    psi0: np.ndarray,
    hbar: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute discrete spectral weights from a Hermitian Hamiltonian."""
    if hbar == 0:
        raise ValueError("hbar must be non-zero")
    eigenvalues, eigenvectors = np.linalg.eigh(H)
    omega = eigenvalues / hbar
    coeffs = eigenvectors.conj().T @ psi0
    amplitudes = np.abs(coeffs) ** 2
    total = np.sum(amplitudes)
    if total > 0:
        amplitudes = amplitudes / total
    return omega, amplitudes


def compute_spectrum_symbolic(
    J: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Return modal frequencies and damping estimates from a Jacobian."""
    from scipy.linalg import eig
    eigenvalues, _ = eig(J)
    frequencies = np.imag(eigenvalues)
    damping = -np.real(eigenvalues)
    return frequencies, damping


def build_discrete_spectrum(
    omega_n: np.ndarray,
    amplitudes: np.ndarray,
    omega_grid: np.ndarray,
    width: float = 1e-6,
) -> np.ndarray:
    """Build a normalized spectrum from discrete Lorentzian peaks."""
    omega_n = np.asarray(omega_n, dtype=float)
    amplitudes = np.asarray(amplitudes, dtype=float)
    omega_grid = np.asarray(omega_grid, dtype=float)
    if not np.isfinite(width) or width <= 0:
        raise ValueError("width must be finite and positive")
    if omega_n.ndim != 1 or amplitudes.ndim != 1:
        raise ValueError("omega_n and amplitudes must be one-dimensional")
    if len(omega_n) == 0 or len(omega_n) != len(amplitudes):
        raise ValueError("omega_n and amplitudes must have equal non-zero lengths")
    if not np.all(np.isfinite(omega_n)):
        raise ValueError("omega_n values must be finite")
    if not np.all(np.isfinite(amplitudes)) or np.any(amplitudes < 0):
        raise ValueError("amplitudes must be finite and non-negative")
    if omega_grid.ndim != 1 or len(omega_grid) < 2:
        raise ValueError("omega_grid must be one-dimensional with at least two points")
    _validate_grid(omega_grid)
    S = np.zeros_like(omega_grid, dtype=complex)
    for w, a in zip(omega_n, amplitudes):
        S += a / ((omega_grid - w) ** 2 + width**2)
    return normalize_spectrum(S, omega_grid)


def build_spectrum_from_descriptor(
    spectrum: Dict[str, Any],
    omega_grid: Optional[np.ndarray] = None,
    n_samples: int = 4000,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build a complex spectrum on a log-spaced grid from a registry descriptor.

    Descriptor keys:
      - peak_centers: positive peak locations
      - peak_widths: widths in log10-frequency units
      - peak_weights: non-negative relative weights
    """
    centers = np.asarray(spectrum.get("peak_centers", [1.0]), dtype=float)
    widths = np.asarray(spectrum.get("peak_widths", [1.0]), dtype=float)
    weights = np.asarray(spectrum.get("peak_weights", [1.0]), dtype=float)

    if centers.ndim != 1 or widths.ndim != 1 or weights.ndim != 1:
        raise ValueError("peak descriptor arrays must be one-dimensional")
    if not (len(centers) == len(widths) == len(weights)) or len(centers) == 0:
        raise ValueError("peak_centers, peak_widths, and peak_weights must have equal non-zero lengths")
    if np.any(~np.isfinite(centers)) or np.any(centers <= 0):
        raise ValueError("peak centers must be finite and positive")
    if np.any(~np.isfinite(widths)) or np.any(widths <= 0):
        raise ValueError("peak widths must be finite and positive")
    if np.any(~np.isfinite(weights)) or np.any(weights < 0) or np.sum(weights) <= 0:
        raise ValueError("peak weights must be finite, non-negative, and have a positive sum")
    weights = weights / np.sum(weights)

    if omega_grid is None:
        if n_samples < 2:
            raise ValueError("n_samples must be at least 2")
        lo = max(centers.min() / 100, 1e-14)
        hi = centers.max() * 100
        omega_grid = np.logspace(np.log10(lo), np.log10(hi), n_samples)
    else:
        omega_grid = np.asarray(omega_grid, dtype=float)
        _validate_grid(omega_grid)
        if np.any(omega_grid <= 0):
            raise ValueError("omega_grid values must be positive for logarithmic descriptors")

    log_om = np.log10(omega_grid)
    S = np.zeros_like(omega_grid, dtype=complex)
    for center, width, weight in zip(centers, widths, weights):
        S += weight * np.exp(-0.5 * ((log_om - np.log10(center)) / width) ** 2)

    return omega_grid, normalize_spectrum(S, omega_grid)


def qualitative_spectrum(theory_type: str) -> dict:
    """Return a qualitative, illustrative spectrum preset."""
    presets = {
        "classical": {"omega_range": (1e-10, 1e-5), "width_orders": 1, "shape": "narrow",
                      "description": "Classical mechanics – narrow spectrum at low Omega"},
        "quantum": {"omega_range": (1e-5, 1e-1), "width_orders": 3, "shape": "discrete",
                    "description": "Quantum mechanics – discrete spectrum"},
        "relativity": {"omega_range": (1e-7, 1e-3), "width_orders": 2, "shape": "medium",
                       "description": "Relativity – medium spectrum"},
        "thermodynamics": {"omega_range": (1e-10, 1e-6), "width_orders": 2, "shape": "broad",
                           "description": "Thermodynamics – broad spectrum at low Omega"},
        "quantum_gravity": {"omega_range": (1e-3, 1e1), "width_orders": 4, "shape": "peaks",
                            "description": "Quantum gravity – spectrum with topological peaks"},
        "phi_theory": {"omega_range": (1e-12, 1e2), "width_orders": 6, "shape": "broad_with_peaks",
                       "description": "Phi-Theory – broad spectrum with Phi-peaks"},
    }
    return presets.get(theory_type.lower(), {
        "omega_range": (1e-10, 1e10), "width_orders": 3, "shape": "unknown",
        "description": "Unknown type – use explicit or symbolic method",
    })
