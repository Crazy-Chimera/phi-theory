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
    if not np.all(np.isfinite(S)):
        raise ValueError("S values must be finite")
    _validate_grid(omega)
    if len(omega) < 2:
        return S.copy()
    # Scale first: squaring large finite samples can overflow, while squaring
    # tiny samples can underflow to zero even when the normalized shape is valid.
    # Use the largest component rather than abs(S): hypot-based complex
    # magnitudes can overflow for finite real/imaginary components near float max.
    scale = (
        max(float(np.max(np.abs(S.real))), float(np.max(np.abs(S.imag))))
        if len(S)
        else 0.0
    )
    if scale == 0:
        return S.copy()
    scaled = S / scale
    norm_sq = float(trapezoid(np.abs(scaled) ** 2, x=omega))
    if not np.isfinite(norm_sq):
        raise ValueError("spectrum norm must be finite")
    if norm_sq <= 0:
        return S.copy()
    return scaled / np.sqrt(norm_sq)


def compute_spectrum_explicit(
    H: np.ndarray,
    psi0: np.ndarray,
    hbar: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute normalized discrete spectral weights from a Hermitian Hamiltonian."""
    H = np.asarray(H)
    psi0 = np.asarray(psi0)
    if H.ndim != 2 or H.shape[0] == 0 or H.shape[0] != H.shape[1]:
        raise ValueError("H must be a non-empty square matrix")
    if not np.all(np.isfinite(H)):
        raise ValueError("H values must be finite")
    if not np.allclose(H, H.conj().T):
        raise ValueError("H must be Hermitian")
    if psi0.ndim != 1 or len(psi0) != H.shape[0]:
        raise ValueError("psi0 must be a one-dimensional vector matching H")
    if not np.all(np.isfinite(psi0)):
        raise ValueError("psi0 values must be finite")
    if not np.isscalar(hbar) or not np.isreal(hbar) or not np.isfinite(hbar) or hbar == 0:
        raise ValueError("hbar must be finite, real, and non-zero")

    eigenvalues, eigenvectors = np.linalg.eigh(H)
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        omega = eigenvalues / hbar
    if not np.all(np.isfinite(omega)):
        raise ValueError("computed frequencies must be finite")

    # Scale the state before projection and the coefficients before squaring.
    # This preserves normalized weights while avoiding overflow for large states.
    state_scale = float(np.max(np.abs(psi0)))
    if state_scale == 0:
        return omega, np.zeros_like(eigenvalues, dtype=float)
    scaled_state = psi0 / state_scale
    coeffs = eigenvectors.conj().T @ scaled_state
    coeff_scale = float(np.max(np.abs(coeffs)))
    if coeff_scale == 0:
        return omega, np.zeros_like(eigenvalues, dtype=float)
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        scaled_amplitudes = np.abs(coeffs / coeff_scale) ** 2
        total = float(np.sum(scaled_amplitudes))
    if not np.isfinite(total) or total <= 0:
        raise ValueError("computed spectral weights must have a finite positive sum")
    amplitudes = scaled_amplitudes / total
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

    # Scale before summing so large finite amplitudes cannot overflow. A zero
    # total carries no spectral information and must not masquerade as a
    # successfully normalized spectrum.
    amplitude_scale = float(np.max(amplitudes))
    if amplitude_scale <= 0:
        raise ValueError("amplitudes must have a positive sum")
    scaled_amplitudes = amplitudes / amplitude_scale
    scaled_total = float(np.sum(scaled_amplitudes))
    if not np.isfinite(scaled_total) or scaled_total <= 0:
        raise ValueError("amplitudes must have a finite positive sum")
    scaled_amplitudes = scaled_amplitudes / scaled_total

    # The common width^2 factor cancels during final normalization. Evaluating
    # 1 / (1 + (delta / width)^2) avoids squaring large frequencies or widths.
    S = np.zeros_like(omega_grid, dtype=float)
    with np.errstate(over="ignore", under="ignore", invalid="ignore", divide="ignore"):
        for w, a in zip(omega_n, scaled_amplitudes):
            delta = omega_grid - w
            ratio = delta / width
            profile = 1.0 / (1.0 + ratio * ratio)
            S += a * profile
    if not np.all(np.isfinite(S)) or not np.any(S > 0):
        raise ValueError("discrete spectrum is not representable on omega_grid")
    return normalize_spectrum(S.astype(complex), omega_grid)


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
    if not np.all(np.isfinite(weights)) or np.any(weights < 0):
        raise ValueError("peak weights must be finite and non-negative")
    # Finite entries can still overflow when summed; reject that instead of
    # dividing by infinity and silently producing an all-zero spectrum.
    with np.errstate(over="ignore", invalid="ignore"):
        weight_sum = float(np.sum(weights))
    if not np.isfinite(weight_sum) or weight_sum <= 0:
        raise ValueError("peak weights must have a finite positive sum")
    weights = weights / weight_sum

    if omega_grid is None:
        if not isinstance(n_samples, (int, np.integer)) or isinstance(n_samples, bool) or n_samples < 2:
            raise ValueError("n_samples must be an integer of at least 2")
        lo = max(centers.min() / 100, 1e-14)
        hi = centers.max() * 100
        omega_grid = np.logspace(np.log10(lo), np.log10(hi), n_samples)
    else:
        omega_grid = np.asarray(omega_grid, dtype=float)
        if omega_grid.ndim != 1 or len(omega_grid) < 2:
            raise ValueError("omega_grid must be one-dimensional with at least two points")
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
