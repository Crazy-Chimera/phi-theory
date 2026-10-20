# Prediction registry audit (P1–P6)

**Status: documentary audit of the current registry, not an independent experimental review.** This document separates stored numerical entries from predictions that can presently be derived from the documented Phi-Theory equations.

## Executive finding

The prediction registry contains numerical spectral-overlap scores, Ω-band endpoints, deviation targets, and falsification statements for P1–P6. The mathematical specification audit finds that the core field dynamics are not yet closed, the displayed master-equation ansatz is not derived from the displayed action, and the Ω-to-laboratory mapping is missing. Consequently, the registry's numerical scores and bands should be treated as outputs of the current qualitative descriptors and analysis conventions—not as empirical evidence or physical effect predictions.

## Entry-by-entry status

| ID | Stored target / topic | Current interpretation | Required before confirmatory use |
|---|---|---|---|
| P1 | ΔA/A_Planck = 0.01; Phi-Theory–LQG | Target is not derived from the documented equations; Planck-regime observable and dataset are not operationally specified. | Shared observable, complete model, derivation, data source, uncertainty and decision rule. |
| P2 | ΔR = 0.05; mesoscopic quantum dynamics | Explicitly blocked. R is not operationally defined and Ω is not mapped to controls. | Follow docs/prediction_validation_P2.md and docs/experiment_P2_mesoscopic.md. |
| P3 | Δy_f/y_f = 10⁻¹²; Phi-Theory–Standard Model | No interaction term or derivation connects Φ to a measurable Yukawa shift in the current specification. | Explicit coupling, observable, derivation, constraints, uncertainties and a feasible analysis plan. |
| P4 | Δα/α = 10⁻¹⁵; Phi-Theory–QED | No derived Φ-dependent correction to α or the electron anomaly is specified. The stored falsification threshold also needs a consistent derivation and sensitivity argument. | Explicit correction model, units/scale dependence, independent bounds, calibration and statistical design. |
| P5 | ΔG/G = 10⁻¹⁰; Phi-Theory–GR | G(Φ) is asserted as a possibility but no functional form or derived constraint is provided. The stated falsification threshold is not shown to follow from the model. | Full gravity-plus-scalar action, field equations, parameter constraints and a defined Φ proxy. |
| P6 | ΔS_classical = 0.1; classical–quantum boundary | Observable and target are not operationally defined; a zero spectral score is an algorithmic descriptor, not evidence of absence of a physical effect. | Definition of S, model-derived prediction, platform-specific baseline and a falsifiable decision rule. |

## Interpretation rules

1. A stored number is not a prediction merely because it appears in YAML or is consumed by code.
2. A spectral overlap score computed from chosen descriptors is a property of those descriptors and the algorithm. It is not a probability, confidence level, or measured resonance.
3. A falsification statement is not operational unless the alternative predicts a defined observable with a quantified effect or distribution and the experiment can exclude it at a stated level.
4. The statuses untested, undecided, and blocked are not interchangeable. Use blocked in planning documents when essential model specification is absent; do not claim empirical confirmation or falsification.
5. Do not replace unsupported values with new guessed values. Preserve their provenance and label them as provisional or unsupported until a derivation exists.

## Registry schema additions (version 1.2.0)

The registry now records the provenance and operational readiness of each P1–P6 entry using these fields:

- `prediction_basis`: currently labels entries as provisional descriptor outputs rather than derived physical predictions.
- `R_spectral_interpretation`: explicitly marks the overlap score as a model-internal descriptor, not a probability or empirical measurement.
- `deviation_basis`: marks stored deviation targets as provisional and unsupported until derived.
- `observable_definition`, `derivation_reference`, and `lab_mapping_reference`: currently null where the registry has no validated operational definition, derivation, or Ω-to-laboratory mapping.
- `status_reason`: states the principal scientific readiness limitation for each entry.

The existing numerical values and workflow statuses are retained for traceability; they have not been reinterpreted as validated forecasts. Null fields are intentional gaps, not implicit evidence or permission to infer missing physics. The registry schema change documents missing support and does not itself close any model or experimental readiness gate.

## Scope

This audit is based on the repository's current registry and mathematical specification. It does not establish that Phi-Theory is true or false, nor does it replace a literature review or independent domain-expert assessment.

## Feedback status is workflow metadata, not scientific validation

The feedback API requires an `evidence_reference` when a caller sets a prediction to `confirmed` or `falsified`. The reference is retained in feedback and resonance-log records to improve traceability. This is a provenance guardrail only:

- The software checks that a reference is present; it does not validate that the reference resolves, that its contents are immutable, or that the referenced material is scientifically adequate.
- A URL, fixture URI, file path, or other pointer is not itself evidence that a prediction is true or false.
- The status label records a workflow decision made by a caller. It must not be presented as an automated scientific conclusion.
- A responsible status change should point to the preregistration, dataset, analysis/code version, primary result, uncertainty, and decision rule that supports the assessment. Independent review and reproducibility remain necessary.
- Dry-run tests and synthetic fixture references validate software behaviour only; they are not empirical evidence.

Do not strengthen this check into a claim of scientific verification unless a separate, explicit evidence-review process is defined and implemented. The API's reference requirement intentionally does not infer evidence quality from a nonempty string.

## Feedback persistence, journal recovery, and remaining limits

A non-dry-run `apply_feedback()` operation stages the prediction registry and resonance log, records their original contents in a transaction journal, and then replaces the target files. If a replacement fails, recovery attempts to restore both original snapshots. On startup/entry, an interrupted journal can be used to recover the original state. Recovery skips a target whose current bytes already match its snapshot, avoiding unnecessary replacement of an unchanged file. The journal is retained until recovery has restored both targets.

This is stronger than independent file replacement, but it is **not a demonstrated crash-atomic multi-file transaction**. The two YAML files remain separate filesystem objects; abrupt termination, power loss, filesystem or storage failures, and durability ordering around file and directory metadata have not been proven safe by a full durability protocol. The journal itself may not survive every hardware/filesystem failure. The test suite's failure-injection and interrupted-recovery tests validate the exercised software paths, not every possible crash state.

After an exception indicating that recovery failed, inspect the journal and both YAML files before retrying. Do not assume either file changed or remained unchanged without checking. Dry-run mode avoids persistence writes, but does not validate filesystem durability. Passing tests and successful recovery are software reliability results only; they do not validate the theory or any prediction scientifically.

## Operational acceptance gate

Use [Prediction readiness gate](prediction_readiness_gate.md) for the shared acceptance criteria and prediction-specific evidence required before moving P1–P6 from blocked status toward design review, preregistration, testing, or independent reproduction. It is intended to make status transitions auditable; it does not replace the equation-level closure work or supply missing physical assumptions.