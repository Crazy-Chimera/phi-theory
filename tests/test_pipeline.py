"""Lightweight tests for Omega-RE pipeline (no network)."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import numpy as np
from core.spectrum import normalize_spectrum, build_spectrum_from_descriptor
from core.resonance import compute_resonance, qualitative_resonance
from core.emergence import identify_bands, compute_kernel
from analysis.feedback import load_predictions, apply_feedback, summary

def test_normalize_spectrum():
    omega = np.linspace(0.1, 10, 500)
    S = np.exp(-((omega - 3) ** 2) / 2) + 0j
    Sn = normalize_spectrum(S, omega)
    domega = omega[1] - omega[0]
    nrm = np.sum(np.abs(Sn) ** 2) * domega
    assert abs(nrm - 1.0) < 1e-6

def test_build_descriptor_and_resonance():
    spec = {"peak_centers": [0.001, 0.01], "peak_widths": [0.5, 0.5], "peak_weights": [0.5, 0.5]}
    omega, S = build_spectrum_from_descriptor(spec, n_samples=2000)
    assert compute_resonance(S, S, omega) > 0.99

def test_qualitative_and_bands():
    assert qualitative_resonance((1e-5, 1e-1), (1e-5, 1e-1)) > 0.5
    omega = np.logspace(-3, 1, 1000)
    R = np.exp(-(np.log10(omega) - 0.0) ** 2 / 0.5)
    assert len(identify_bands(omega, R, threshold=0.5)) >= 1

def test_kernel_finite():
    omega = np.linspace(1, 10, 200)
    K = compute_kernel(np.ones_like(omega) + 0j, 0.5 * np.ones_like(omega) + 0j)
    assert np.all(np.isfinite(K))

def test_predictions_load_and_dry_run():
    data = load_predictions()
    assert len(data.get("predictions", [])) >= 1
    pid = data["predictions"][0]["id"]
    before = summary()
    apply_feedback(pid, "confirmed", note="test", dry_run=True)
    assert summary() == before

if __name__ == "__main__":
    test_normalize_spectrum()
    test_build_descriptor_and_resonance()
    test_qualitative_and_bands()
    test_kernel_finite()
    test_predictions_load_and_dry_run()
    print("All pipeline tests passed.")
