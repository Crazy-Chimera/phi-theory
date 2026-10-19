"""
Ω-RE Core – spectral decomposition, resonance and emergent derivation.
"""

from .spectrum import compute_spectrum_explicit, compute_spectrum_symbolic, normalize_spectrum
from .resonance import compute_resonance, resonance_matrix
from .emergence import compute_kernel, analyze_kernel, identify_bands

__all__ = [
    "compute_spectrum_explicit",
    "compute_spectrum_symbolic",
    "normalize_spectrum",
    "compute_resonance",
    "resonance_matrix",
    "compute_kernel",
    "analyze_kernel",
    "identify_bands",
]
