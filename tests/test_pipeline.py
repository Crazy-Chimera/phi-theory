"""Tests for the Omega-RE numerical and feedback pipeline."""
from __future__ import annotations

import sys
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.integrate import trapezoid
import yaml
import analysis.feedback as feedback_module
from core.spectrum import normalize_spectrum, build_spectrum_from_descriptor
from core.resonance import compute_resonance, qualitative_resonance
from core.emergence import identify_bands, compute_kernel, local_overlap_profile
from analysis.feedback import load_predictions, apply_feedback, summary
from analysis.predictions import save_predictions as save_prediction_records


def test_normalize_spectrum_nonuniform_grid():
    omega = np.logspace(-3, 2, 500)
    spectrum = np.exp(-((np.log10(omega) - 0.2) ** 2)) + 0j
    normalized = normalize_spectrum(spectrum, omega)
    norm = trapezoid(np.abs(normalized) ** 2, x=omega)
    assert abs(norm - 1.0) < 1e-10


def test_resonance_invariants_on_nonuniform_grid():
    omega = np.logspace(-4, 3, 1000)
    spectrum = np.exp(-((np.log10(omega) - 0.3) ** 2)) + 0j
    orthogonal_like = np.exp(-((np.log10(omega) - 2.0) ** 2)) + 0j
    assert abs(compute_resonance(spectrum, spectrum, omega) - 1.0) < 1e-10
    score = compute_resonance(spectrum, orthogonal_like, omega)
    assert 0.0 <= score <= 1.0
    assert compute_resonance(np.zeros_like(spectrum), spectrum, omega) == 0.0


def test_resonance_rejects_invalid_grids():
    with np.testing.assert_raises(ValueError):
        compute_resonance(np.ones(3), np.ones(3), np.array([1.0, 1.0, 2.0]))
    with np.testing.assert_raises(ValueError):
        normalize_spectrum(np.ones(3), np.array([1.0, 3.0, 2.0]))


def test_build_descriptor_and_resonance():
    descriptor = {
        "peak_centers": [0.001, 0.01],
        "peak_widths": [0.5, 0.5],
        "peak_weights": [0.5, 0.5],
    }
    omega, spectrum = build_spectrum_from_descriptor(descriptor, n_samples=2000)
    assert compute_resonance(spectrum, spectrum, omega) > 0.999999


def test_invalid_descriptor_rejected():
    descriptor = {"peak_centers": [0.0], "peak_widths": [0.5], "peak_weights": [1.0]}
    with np.testing.assert_raises(ValueError):
        build_spectrum_from_descriptor(descriptor, n_samples=100)


def test_qualitative_and_bands():
    assert qualitative_resonance((1e-5, 1e-1), (1e-5, 1e-1)) > 0.5
    omega = np.logspace(-3, 1, 1000)
    curve = np.exp(-(np.log10(omega) ** 2) / 0.5)
    assert len(identify_bands(omega, curve, threshold=0.5)) >= 1



def test_local_overlap_profile_is_bounded_and_peak_normalized():
    omega = np.logspace(-3, 2, 501)
    S1 = np.exp(-((np.log10(omega) - 0.5) ** 2) / 0.2) + 0j
    S2 = np.exp(-((np.log10(omega) - 0.5) ** 2) / 0.3) + 0j
    profile = local_overlap_profile(S1, S2, omega, smoothing_window=21)
    assert profile.shape == omega.shape
    assert np.all(np.isfinite(profile))
    assert np.all((profile >= 0.0) & (profile <= 1.0))
    assert abs(float(profile.max()) - 1.0) < 1e-12

    zeros = local_overlap_profile(np.zeros_like(S1), S2, omega)
    assert np.all(zeros == 0.0)


def test_kernel_finite():
    omega = np.linspace(1, 10, 200)
    kernel = compute_kernel(np.ones_like(omega) + 0j, 0.5 * np.ones_like(omega) + 0j)
    assert np.all(np.isfinite(kernel))


def test_dry_run_does_not_write_files():
    predictions_path = feedback_module.PREDICTIONS_PATH
    resonances_path = feedback_module.RESONANCES_PATH
    before_predictions = predictions_path.read_bytes()
    before_resonances = resonances_path.read_bytes() if resonances_path.exists() else None
    prediction_id = load_predictions()["predictions"][0]["id"]

    result = apply_feedback(
        prediction_id,
        "confirmed",
        note="dry-run test",
        dry_run=True,
        evidence_reference="test-fixture://dry-run",
    )

    assert result["status"] == "confirmed"
    assert predictions_path.read_bytes() == before_predictions
    assert (resonances_path.read_bytes() if resonances_path.exists() else None) == before_resonances



def test_feedback_status_does_not_change_spectral_band_values():
    prediction = load_predictions()["predictions"][0]
    original_band = dict(prediction.get("band", {}))

    result = apply_feedback(
        prediction["id"],
        "confirmed",
        note="workflow status must not rescale model output",
        dry_run=True,
        evidence_reference="test-fixture://no-band-mutation",
    )

    assert result.get("band", {}) == original_band


def test_predictions_load_and_dry_run():
    data = load_predictions()
    predictions = data.get("predictions", [])
    assert predictions, "Expected at least one registered prediction"
    prediction_id = predictions[0]["id"]
    before = summary()
    apply_feedback(prediction_id, "undecided", note="test", dry_run=True)
    assert summary() == before




def test_confirmation_and_falsification_require_evidence_reference():
    prediction_id = load_predictions()["predictions"][0]["id"]
    for status in ("confirmed", "falsified"):
        with np.testing.assert_raises_regex(ValueError, "evidence_reference"):
            apply_feedback(prediction_id, status, dry_run=True)

        result = apply_feedback(
            prediction_id,
            status,
            dry_run=True,
            evidence_reference="test-fixture://evidence",
        )
        assert result["feedback"]["evidence_reference"] == "test-fixture://evidence"


def test_prediction_save_preserves_registry_metadata():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "predictions.yaml"
        original = {
            "version": "1.1.0",
            "updated": "2026-10-19",
            "description": "Predictions from spectral Ω-RE bands",
            "custom_metadata": {"source": "audit"},
            "predictions": [{"id": "P-old", "status": "untested"}],
        }
        path.write_text(yaml.safe_dump(original, allow_unicode=True), encoding="utf-8")

        replacement = [{"id": "P-new", "status": "undecided"}]
        save_prediction_records(replacement, path)
        saved = yaml.safe_load(path.read_text(encoding="utf-8"))

        assert saved["version"] == "1.1.0"
        assert saved["description"] == original["description"]
        assert saved["custom_metadata"] == original["custom_metadata"]
        assert saved["predictions"] == replacement
        assert saved["updated"] != original["updated"]


if __name__ == "__main__":
    test_normalize_spectrum_nonuniform_grid()
    test_resonance_invariants_on_nonuniform_grid()
    test_resonance_rejects_invalid_grids()
    test_build_descriptor_and_resonance()
    test_invalid_descriptor_rejected()
    test_qualitative_and_bands()
    test_local_overlap_profile_is_bounded_and_peak_normalized()
    test_kernel_finite()
    test_dry_run_does_not_write_files()
    test_predictions_load_and_dry_run()
    print("All pipeline tests passed.")
