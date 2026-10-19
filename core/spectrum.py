"""
Spectral decomposition of theories (Ω-spectrum).

T(Ω) = ∫ S_T(ω) · e^{iωΩ} dω
"""

from __future__ import annotations

import numpy as np
from typing import Tuple, Optional


def normalize_spectrum(S: np.ndarray, omega: np.ndarray) -> np.ndarray:
    """Normalize spectrum so that ∫|S|² dω = 1."""
    if len(omega) < 2:
        return S
    dω = omega[1] - omega[0]
    norm = np.sqrt(np.sum(np.abs(S) ** 2) * dω)
    if norm == 0:
        return S
    return S / norm


def compute_spectrum_explicit(
    H: np.ndarray,
    psi0: np.ndarray,
    hbar: float = 1.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Explicit spectral decomposition from a Hamiltonian.

    Args:
        H: Hamiltonian (Hermitian matrix)
        psi0: initial state (vector)
        hbar: Planck constant (default 1)

    Returns:
        omega: frequencies (eigenvalues / ℏ)
        amplitudes: |c_n|² (normalized)
    """
    eigenvalues, eigenvectors = np.linalg.eigh(H)
    omega = eigenvalues / hbar
    coeffs = eigenvectors.conj().T @ psi0
    amplitudes = np.abs(coeffs) ** 2
    amplitudes /= np.sum(amplitudes)
    return omega, amplitudes


def compute_spectrum_symbolic(
    J: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Symbolic / linearization analysis from a Jacobian matrix.

    Returns:
        frequencies: Im(λ)
        damping: -Re(λ)
    """
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
    """
    Build a continuous spectrum from discrete peaks (Lorentzian functions).
    """
    S = np.zeros_like(omega_grid, dtype=complex)
    for ω, A in zip(omega_n, amplitudes):
        S += A / ((omega_grid - ω) ** 2 + width**2 + 0j)
    return normalize_spectrum(S, omega_grid)


def qualitative_spectrum(theory_type: str) -> dict:
    """
    Qualitative spectrum estimate according to theory type.
    """
    presets = {
        "classical": {
            "omega_range": (1e-10, 1e-5),
            "width_orders": 1,
            "shape": "narrow",
            "description": "Classical mechanics – narrow spectrum at low Ω",
        },
        "quantum": {
            "omega_range": (1e-5, 1e-1),
            "width_orders": 3,
            "shape": "discrete",
            "description": "Quantum mechanics – discrete spectrum",
        },
        "relativity": {
            "omega_range": (1e-7, 1e-3),
            "width_orders": 2,
            "shape": "medium",
            "description": "Relativity – medium spectrum",
        },
        "thermodynamics": {
            "omega_range": (1e-10, 1e-6),
            "width_orders": 2,
            "shape": "broad",
            "description": "Thermodynamics – broad spectrum at low Ω",
        },
        "quantum_gravity": {
            "omega_range": (1e-3, 1e1),
            "width_orders": 4,
            "shape": "peaks",
            "description": "Quantum gravity – spectrum with topological peaks",
        },
        "phi_theory": {
            "omega_range": (1e-12, 1e2),
            "width_orders": 6,
            "shape": "broad_with_peaks",
            "description": "Phi-Theory – broad spectrum with Φ-peaks",
        },
    }
    return presets.get(theory_type.lower(), {
        "omega_range": (1e-10, 1e10),
        "width_orders": 3,
        "shape": "unknown",
        "description": "Unknown type – use explicit or symbolic method",
    })
