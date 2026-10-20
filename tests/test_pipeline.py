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
from core.spectrum import normalize_spectrum, build_spectrum_from_descriptor, build_discrete_spectrum
from core.resonance import compute_resonance, qualitative_resonance, interpolate_to_grid
from core.emergence import identify_bands, compute_kernel, local_overlap_profile, analyze_kernel
from analysis.feedback import load_predictions, apply_feedback, summary
from analysis.predictions import save_predictions as save_prediction_records



def test_explicit_spectrum_validates_inputs_and_stabilizes_weights():
    from core.spectrum import compute_spectrum_explicit

    H = np.diag([1.0, 2.0])
    omega, weights = compute_spectrum_explicit(H, np.array([1e308, 1e308]))
    assert np.all(np.isfinite(omega))
    assert np.all(np.isfinite(weights))
    assert abs(float(np.sum(weights)) - 1.0) < 1e-12

    _, zero_weights = compute_spectrum_explicit(H, np.zeros(2))
    assert np.all(zero_weights == 0.0)

    invalid_cases = [
        (np.ones((2, 3)), np.ones(2), 1.0, "non-empty square"),
        (np.array([[1.0, 2.0], [0.0, 1.0]]), np.ones(2), 1.0, "Hermitian"),
        (H, np.ones((2, 1)), 1.0, "one-dimensional vector"),
        (H, np.array([1.0, np.inf]), 1.0, "psi0 values must be finite"),
        (H, np.ones(2), 0.0, "hbar must be finite"),
        (H, np.ones(2), np.inf, "hbar must be finite"),
        (H, np.ones(2), 1e-320, "computed frequencies must be finite"),
    ]
    for matrix, state, hbar, message in invalid_cases:
        with np.testing.assert_raises_regex(ValueError, message):
            compute_spectrum_explicit(matrix, state, hbar=hbar)

def test_normalize_spectrum_scales_extreme_finite_values():
    omega = np.linspace(0.0, 1.0, 101)
    for scale in (1e308, 1e-308):
        spectrum = normalize_spectrum(np.full(omega.shape, scale, dtype=complex), omega)
        assert np.all(np.isfinite(spectrum))
        assert abs(float(trapezoid(np.abs(spectrum) ** 2, x=omega)) - 1.0) < 1e-12


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


def test_resonance_rejects_nonfinite_inputs():
    with np.testing.assert_raises_regex(ValueError, "omega values must be finite"):
        compute_resonance(np.ones(2), np.ones(2), np.array([1.0, np.nan]))
    with np.testing.assert_raises_regex(ValueError, "S1 and S2 values must be finite"):
        compute_resonance(np.array([1.0, np.inf]), np.ones(2), np.array([1.0, 2.0]))
    with np.testing.assert_raises_regex(ValueError, "omega_src and S_src must have equal non-zero lengths"):
        interpolate_to_grid(np.array([]), np.array([]), np.array([1.0, 2.0]))
    with np.testing.assert_raises_regex(ValueError, "omega values must be finite"):
        interpolate_to_grid(np.array([1.0, 2.0]), np.ones(2), np.array([1.0, np.inf]))


def test_resonance_handles_overflowing_intermediates():
    omega = np.array([1.0, 2.0])
    extreme = np.array([1e200, 1e200])
    assert compute_resonance(extreme, extreme, omega) == 0.0



def test_normalize_spectrum_rejects_nonfinite_inputs():
    with np.testing.assert_raises_regex(ValueError, "S values must be finite"):
        normalize_spectrum(np.array([1.0, np.nan]), np.array([1.0, 2.0]))
    with np.testing.assert_raises_regex(ValueError, "omega values must be finite"):
        normalize_spectrum(np.array([1.0, 1.0]), np.array([1.0, np.inf]))

    # Finite amplitudes whose unscaled squares would overflow remain normalizable.
    omega = np.array([1.0, 2.0])
    normalized = normalize_spectrum(np.array([1e308, 1e308]), omega)
    assert np.all(np.isfinite(normalized))
    assert abs(float(trapezoid(np.abs(normalized) ** 2, x=omega)) - 1.0) < 1e-12


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


def test_descriptor_rejects_overflowing_weight_sum():
    descriptor = {
        "peak_centers": [1.0, 2.0],
        "peak_widths": [0.5, 0.5],
        "peak_weights": [1e308, 1e308],
    }
    with np.testing.assert_raises_regex(ValueError, "finite positive sum"):
        build_spectrum_from_descriptor(descriptor, n_samples=100)


def test_qualitative_and_bands():
    assert qualitative_resonance((1e-5, 1e-1), (1e-5, 1e-1)) > 0.5
    omega = np.logspace(-3, 1, 1000)
    curve = np.exp(-(np.log10(omega) ** 2) / 0.5)
    assert len(identify_bands(omega, curve, threshold=0.5)) >= 1



def test_descriptor_rejects_undersized_explicit_grid():
    descriptor = {
        "peak_centers": [1.0],
        "peak_widths": [0.5],
        "peak_weights": [1.0],
    }
    for grid in (np.array([]), np.array([1.0])):
        with np.testing.assert_raises_regex(ValueError, "at least two points"):
            build_spectrum_from_descriptor(descriptor, omega_grid=grid)


def test_descriptor_rejects_invalid_sample_count():
    descriptor = {
        "peak_centers": [1.0],
        "peak_widths": [0.5],
        "peak_weights": [1.0],
    }
    for n_samples in (1, 2.5, True):
        with np.testing.assert_raises_regex(ValueError, "integer of at least 2"):
            build_spectrum_from_descriptor(descriptor, n_samples=n_samples)



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


def test_overlap_and_band_functions_reject_invalid_inputs():
    with np.testing.assert_raises_regex(ValueError, "S1 and S2 values must be finite"):
        local_overlap_profile(np.array([1.0, np.nan]), np.ones(2), np.array([1.0, 2.0]))
    with np.testing.assert_raises_regex(ValueError, "smoothing_window must be a positive integer"):
        local_overlap_profile(np.ones(2), np.ones(2), np.array([1.0, 2.0]), smoothing_window=1.5)
    with np.testing.assert_raises_regex(ValueError, "omega and R must have equal lengths"):
        identify_bands(np.array([1.0, 2.0]), np.array([0.9]))
    with np.testing.assert_raises_regex(ValueError, "omega values must be positive"):
        identify_bands(np.array([0.0, 2.0]), np.array([0.9, 0.9]))
    with np.testing.assert_raises_regex(ValueError, "omega and R values must be finite"):
        identify_bands(np.array([1.0, 2.0]), np.array([0.9, np.inf]))


def test_kernel_functions_reject_invalid_inputs():
    with np.testing.assert_raises_regex(ValueError, "S1 and S2 must have equal lengths"):
        compute_kernel(np.ones(2), np.ones(3))
    with np.testing.assert_raises_regex(ValueError, "S1 and S2 values must be finite"):
        compute_kernel(np.array([1.0, np.nan]), np.ones(2))
    with np.testing.assert_raises_regex(ValueError, "eps must be finite and positive"):
        compute_kernel(np.ones(2), np.ones(2), eps=0.0)
    with np.testing.assert_raises_regex(ValueError, "computed kernel contains non-finite values"):
        compute_kernel(np.array([-1e-10]), np.ones(1), eps=1e-10)
    with np.testing.assert_raises_regex(ValueError, "K and omega must have equal lengths"):
        analyze_kernel(np.ones(2), np.array([1.0]))
    with np.testing.assert_raises_regex(ValueError, "K and omega values must be finite"):
        analyze_kernel(np.array([1.0, np.inf]), np.array([1.0, 2.0]))



def test_discrete_spectrum_rejects_invalid_inputs():
    grid = np.linspace(-2.0, 2.0, 101)
    with np.testing.assert_raises_regex(ValueError, "equal non-zero lengths"):
        build_discrete_spectrum(np.array([0.0, 1.0]), np.array([1.0]), grid)
    with np.testing.assert_raises_regex(ValueError, "finite and positive"):
        build_discrete_spectrum(np.array([0.0]), np.array([1.0]), grid, width=np.nan)
    with np.testing.assert_raises_regex(ValueError, "finite and non-negative"):
        build_discrete_spectrum(np.array([0.0]), np.array([-1.0]), grid)
    with np.testing.assert_raises_regex(ValueError, "finite"):
        build_discrete_spectrum(np.array([np.inf]), np.array([1.0]), grid)
    with np.testing.assert_raises_regex(ValueError, "finite"):
        build_discrete_spectrum(np.array([0.0]), np.array([1.0]), np.array([0.0, np.nan]))

    with np.testing.assert_raises_regex(ValueError, "positive sum"):
        build_discrete_spectrum(np.array([0.0]), np.array([0.0]), grid)

    huge_grid = np.array([1e200, 1e200 + 1e190, 1e200 + 2e190])
    huge_spectrum = build_discrete_spectrum(
        np.array([1e200]), np.array([1e308]), huge_grid, width=1e190
    )
    assert np.all(np.isfinite(huge_spectrum))
    assert abs(float(trapezoid(np.abs(huge_spectrum) ** 2, x=huge_grid)) - 1.0) < 1e-10

    balanced = build_discrete_spectrum(
        np.array([-1.0, 1.0]), np.array([1e308, 1e308]), grid, width=0.05
    )
    assert np.all(np.isfinite(balanced))
    assert abs(float(trapezoid(np.abs(balanced) ** 2, x=grid)) - 1.0) < 1e-10


def test_discrete_spectrum_normalizes_valid_inputs():
    grid = np.linspace(-5.0, 5.0, 1001)
    spectrum = build_discrete_spectrum(
        np.array([-1.0, 1.0]), np.array([0.25, 0.75]), grid, width=0.05
    )
    assert np.all(np.isfinite(spectrum))
    assert abs(float(trapezoid(np.abs(spectrum) ** 2, x=grid)) - 1.0) < 1e-10


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




def test_feedback_rejects_invalid_status_inputs():
    prediction_id = load_predictions()["predictions"][0]["id"]
    for status in ("unknown", "", None, 42):
        with np.testing.assert_raises(ValueError):
            apply_feedback(prediction_id, status, dry_run=True)


def test_feedback_rejects_non_string_evidence_reference():
    prediction_id = load_predictions()["predictions"][0]["id"]
    for reference in (None, 42):
        with np.testing.assert_raises_regex(ValueError, "evidence_reference must be a string"):
            apply_feedback(
                prediction_id,
                "confirmed",
                dry_run=True,
                evidence_reference=reference,
            )


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


def test_feedback_persists_provenance_without_changing_band(tmp_path, monkeypatch):
    predictions_path = tmp_path / "predictions.yaml"
    resonances_path = tmp_path / "resonances.yaml"
    original = {
        "version": "test",
        "custom_metadata": {"origin": "isolated test"},
        "predictions": [
            {
                "id": "P-test",
                "status": "undecided",
                "band": {"low": 0.25, "high": 0.75},
                "custom_field": "preserve me",
            }
        ],
    }
    predictions_path.write_text(
        yaml.safe_dump(original, allow_unicode=True), encoding="utf-8"
    )
    original_log = {
        "version": "log-test",
        "custom_metadata": {"source": "pre-existing log"},
        "entries": [{"prediction_id": "P-existing", "status": "undecided"}],
    }
    resonances_path.write_text(
        yaml.safe_dump(original_log, allow_unicode=True), encoding="utf-8"
    )
    monkeypatch.setattr(feedback_module, "PREDICTIONS_PATH", predictions_path)
    monkeypatch.setattr(feedback_module, "RESONANCES_PATH", resonances_path)

    reference = "test-fixture://persisted-provenance"
    result = apply_feedback(
        "P-test",
        "confirmed",
        note="isolated persistence test",
        evidence_reference=reference,
    )

    saved_predictions = yaml.safe_load(predictions_path.read_text(encoding="utf-8"))
    saved_prediction = saved_predictions["predictions"][0]
    saved_log = yaml.safe_load(resonances_path.read_text(encoding="utf-8"))

    assert result["status"] == "confirmed"
    assert saved_prediction["status"] == "confirmed"
    assert saved_prediction["feedback"]["evidence_reference"] == reference
    assert saved_prediction["band"] == original["predictions"][0]["band"]
    assert saved_prediction["custom_field"] == "preserve me"
    assert saved_predictions["version"] == "test"
    assert saved_predictions["custom_metadata"] == original["custom_metadata"]
    assert saved_log["version"] == "log-test"
    assert saved_log["custom_metadata"] == original_log["custom_metadata"]
    assert saved_log["entries"][0] == original_log["entries"][0]
    assert saved_log["entries"][-1]["evidence_reference"] == reference
    assert saved_log["entries"][-1]["prediction_id"] == "P-test"
    assert saved_log["entries"][-1]["status"] == "confirmed"


def test_malformed_resonance_log_does_not_partially_update_registry(tmp_path, monkeypatch):
    predictions_path = tmp_path / "predictions.yaml"
    resonances_path = tmp_path / "resonances.yaml"
    original = {
        "version": "test",
        "predictions": [{"id": "P-test", "status": "undecided"}],
    }
    predictions_path.write_text(
        yaml.safe_dump(original, allow_unicode=True), encoding="utf-8"
    )
    original_bytes = predictions_path.read_bytes()
    resonances_path.write_text("entries: [unterminated", encoding="utf-8")
    monkeypatch.setattr(feedback_module, "PREDICTIONS_PATH", predictions_path)
    monkeypatch.setattr(feedback_module, "RESONANCES_PATH", resonances_path)

    with np.testing.assert_raises(yaml.YAMLError):
        apply_feedback(
            "P-test",
            "confirmed",
            evidence_reference="test-fixture://malformed-log",
        )

    assert predictions_path.read_bytes() == original_bytes
    assert yaml.safe_load(predictions_path.read_text(encoding="utf-8")) == original


def test_feedback_rolls_back_registry_if_resonance_replace_fails(
    tmp_path, monkeypatch
):
    predictions_path = tmp_path / "predictions.yaml"
    resonances_path = tmp_path / "resonances.yaml"
    original_predictions = {
        "version": "test",
        "predictions": [{"id": "P-test", "status": "undecided"}],
    }
    original_resonances = {
        "version": "test-log",
        "entries": [{"prediction_id": "P-existing", "status": "untested"}],
    }
    predictions_path.write_text(
        yaml.safe_dump(original_predictions), encoding="utf-8"
    )
    resonances_path.write_text(
        yaml.safe_dump(original_resonances), encoding="utf-8"
    )
    prediction_bytes = predictions_path.read_bytes()
    resonance_bytes = resonances_path.read_bytes()
    monkeypatch.setattr(feedback_module, "PREDICTIONS_PATH", predictions_path)
    monkeypatch.setattr(feedback_module, "RESONANCES_PATH", resonances_path)

    real_replace = feedback_module.os.replace

    def fail_resonance_replacement(source, destination):
        if Path(destination) == resonances_path:
            raise OSError("simulated resonance-log replacement failure")
        return real_replace(source, destination)

    monkeypatch.setattr(feedback_module.os, "replace", fail_resonance_replacement)

    with np.testing.assert_raises_regex(OSError, "simulated resonance-log"):
        apply_feedback(
            "P-test",
            "confirmed",
            evidence_reference="test-fixture://replace-failure",
        )

    assert predictions_path.read_bytes() == prediction_bytes
    assert resonances_path.read_bytes() == resonance_bytes
    assert not [path for path in tmp_path.iterdir() if path.name.endswith(".tmp")]



def test_feedback_journal_recovers_interrupted_pair_write(tmp_path, monkeypatch):
    predictions_path = tmp_path / "predictions.yaml"
    resonances_path = tmp_path / "resonances.yaml"
    journal_path = tmp_path / ".feedback-transaction.json"
    original_predictions = b"version: test\\npredictions: []\\n"
    predictions_path.write_bytes(b"partially-updated registry")
    resonances_path.write_bytes(b"partially-updated log")
    journal = {
        "version": 1,
        "originals": {
            "predictions": feedback_module.base64.b64encode(original_predictions).decode("ascii"),
            "resonances": None,
        },
    }
    journal_path.write_text(
        feedback_module.json.dumps(journal),
        encoding="utf-8",
    )
    monkeypatch.setattr(feedback_module, "PREDICTIONS_PATH", predictions_path)
    monkeypatch.setattr(feedback_module, "RESONANCES_PATH", resonances_path)

    feedback_module._recover_interrupted_feedback()

    assert predictions_path.read_bytes() == original_predictions
    assert not resonances_path.exists()
    assert not journal_path.exists()

def test_feedback_staging_failure_leaves_both_files_unchanged(tmp_path, monkeypatch):
    predictions_path = tmp_path / "predictions.yaml"
    resonances_path = tmp_path / "resonances.yaml"
    predictions_path.write_text(
        yaml.safe_dump({
            "version": "test",
            "predictions": [{"id": "P-test", "status": "undecided"}],
        }),
        encoding="utf-8",
    )
    resonances_path.write_text(
        yaml.safe_dump({
            "version": "test-log",
            "entries": [{"prediction_id": "P-existing", "status": "untested"}],
        }),
        encoding="utf-8",
    )
    prediction_bytes = predictions_path.read_bytes()
    resonance_bytes = resonances_path.read_bytes()
    monkeypatch.setattr(feedback_module, "PREDICTIONS_PATH", predictions_path)
    monkeypatch.setattr(feedback_module, "RESONANCES_PATH", resonances_path)

    real_stage = feedback_module._stage_bytes

    def fail_resonance_staging(path, payload):
        if Path(path) == resonances_path:
            raise OSError("simulated resonance-log staging failure")
        return real_stage(path, payload)

    monkeypatch.setattr(feedback_module, "_stage_bytes", fail_resonance_staging)

    with np.testing.assert_raises_regex(OSError, "resonance-log staging failure"):
        apply_feedback(
            "P-test",
            "confirmed",
            evidence_reference="test-fixture://staging-failure",
        )

    assert predictions_path.read_bytes() == prediction_bytes
    assert resonances_path.read_bytes() == resonance_bytes
    assert not [path for path in tmp_path.iterdir() if path.name.endswith(".tmp")]


def test_feedback_reports_rollback_failure_explicitly(tmp_path, monkeypatch):
    predictions_path = tmp_path / "predictions.yaml"
    resonances_path = tmp_path / "resonances.yaml"
    original_predictions = {
        "version": "test",
        "predictions": [{"id": "P-test", "status": "undecided"}],
    }
    original_resonances = {
        "version": "test-log",
        "entries": [{"prediction_id": "P-existing", "status": "untested"}],
    }
    predictions_path.write_text(
        yaml.safe_dump(original_predictions), encoding="utf-8"
    )
    resonances_path.write_text(
        yaml.safe_dump(original_resonances), encoding="utf-8"
    )
    original_log_bytes = resonances_path.read_bytes()
    monkeypatch.setattr(feedback_module, "PREDICTIONS_PATH", predictions_path)
    monkeypatch.setattr(feedback_module, "RESONANCES_PATH", resonances_path)

    real_replace = feedback_module.os.replace
    prediction_replacements = 0

    def fail_resonance_and_rollback(source, destination):
        nonlocal prediction_replacements
        destination = Path(destination)
        if destination == predictions_path:
            prediction_replacements += 1
            # First replacement commits the updated registry; the second is rollback.
            if prediction_replacements == 2:
                raise OSError("simulated rollback failure")
        if destination == resonances_path:
            raise OSError("simulated resonance-log replacement failure")
        return real_replace(source, destination)

    monkeypatch.setattr(feedback_module.os, "replace", fail_resonance_and_rollback)

    with np.testing.assert_raises_regex(
        RuntimeError, "prediction-registry rollback also failed"
    ):
        apply_feedback(
            "P-test",
            "confirmed",
            evidence_reference="test-fixture://rollback-failure",
        )

    # The failure is deliberately unrecoverable in this test: callers must be
    # told to inspect both files rather than assuming the pair was restored.
    saved_predictions = yaml.safe_load(predictions_path.read_text(encoding="utf-8"))
    assert saved_predictions["predictions"][0]["status"] == "confirmed"
    assert resonances_path.read_bytes() == original_log_bytes
    assert not [path for path in tmp_path.iterdir() if path.name.endswith(".tmp")]


if __name__ == "__main__":
    test_normalize_spectrum_nonuniform_grid()
    test_resonance_invariants_on_nonuniform_grid()
    test_resonance_rejects_invalid_grids()
    test_resonance_rejects_nonfinite_inputs()
    test_build_descriptor_and_resonance()
    test_invalid_descriptor_rejected()
    test_descriptor_rejects_overflowing_weight_sum()
    test_qualitative_and_bands()
    test_local_overlap_profile_is_bounded_and_peak_normalized()
    test_overlap_and_band_functions_reject_invalid_inputs()
    test_kernel_functions_reject_invalid_inputs()
    test_kernel_finite()
    test_dry_run_does_not_write_files()
    test_predictions_load_and_dry_run()
    print("All pipeline tests passed.")
