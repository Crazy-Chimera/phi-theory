# Experiment P2 — Mesoscopic Resonance (Phi-Theory ↔ Quantum Mechanics)

| | |
|---|---|
| **Prediction ID** | P2 |
| **Pair** | Phi-Theory ↔ Quantum Mechanics |
| **Spectral R_Ω** | ≈ 0.518 (model-internal descriptor overlap, not a probability) |
| **Band** | Ω ∈ [3.39×10⁻⁵, 0.216], center ≈ 2.71×10⁻³ (coordinate not yet mapped to laboratory units) |
| **Observable** | ΔR (mesoscopic) — operational definition missing |
| **Status** | undecided (planning stage; confirmatory test blocked) |
| **Priority** | Exploratory planning only; not a ranked empirical opportunity until the model is specified |

---

## 1. Scientific goal

Explore whether mesoscopic systems show reproducible residuals from a well-specified standard-quantum baseline, and whether a completed Phi-Theory model predicts those residuals. This is a research question, not an established effect.

Phi-Theory proposes an entanglement-density field Φ and a quantity Ω. The current registry does not yet supply a closed, dimensionally checked dynamical model connecting Φ to standard quantum dynamics or mapping Ω to laboratory controls. The mathematical blockers are documented in [phi_theory_specification_audit.md](phi_theory_specification_audit.md).

## 2. Candidate systems (not a platform selection)

| Platform | Potential experimental capability | Illustrative scale |
|----------|------------------------------------|--------------------|
| Semiconductor quantum dots | Tunable confinement, optical and transport readout | Platform-dependent |
| Superconducting circuits | High-control quantum dynamics and circuit-QED readout | Effective degrees of freedom depend on device |
| Trapped-ion systems | Individual control and entanglement engineering | Platform-dependent |
| Molecular magnets / spin clusters | Controlled mesoscopic spin dynamics | Platform-dependent |
| Nanomechanical resonators | Tests near the quantum–classical boundary | Mass and mode dependent |

No platform is selected. Selection should follow from a derived observable, plausible coupling, available control, and a defensible noise model—not from the spectral overlap score alone.

## 3. Null hypothesis and proposed alternative

**Null:** The selected system is adequately described by a preregistered standard quantum model (Schrödinger or an appropriate open-system/Lindblad model), including calibrated environmental effects and nuisance parameters.

**Alternative:** A fully specified Phi-Theory model predicts a particular residual in a named observable under specified conditions. This alternative is not currently quantitative because the field dynamics, the Ω-to-laboratory mapping, and the observable model are missing.

A possible placeholder expression is

\[
\Delta R=(R_{\mathrm{obs}}-R_{\mathrm{QM}})/R_{\mathrm{QM}}.
\]

This is not operational until both R terms, estimator, units, uncertainty, and data-reduction procedure are defined. The registry's ΔR = 0.05 is unsupported by a derivation and must not be used as a predicted effect size.

## 4. Exploratory protocol outline only

1. Choose a platform only after deriving a measurable coupling and observable.
2. Characterise the standard quantum dynamics and environmental noise.
3. Validate the analysis pipeline using simulated null data and injected effects of known size.
4. If a complete model becomes available, freeze its equations and parameter values before confirmatory data collection.
5. Preregister the primary endpoint, exclusions, sample-size/power calculation, multiplicity handling, and decision rule.
6. Preserve raw data, calibration, code version, dependencies, and analysis outputs for independent reproduction.

Steps 1, 4, and 5 are blocked until the model specification is complete. Simulations validate software behaviour only; they are not evidence for a physical effect.

## 5. Sensitivity requirements — not yet set

No numerical sensitivity target is currently justified. The earlier proposed thresholds (for example, precision of 0.01 or 0.001 in ΔR) are provisional placeholders, not derived requirements. A defensible target requires a dimensioned effect prediction or predicted distribution, a noise model, a chosen statistical test, and a power or exclusion calculation.

## 6. Falsification criteria — not yet operational

The phrase “no deviation in the resonant band” is not a valid quantitative falsification rule until the band is mapped to experimental settings and the model predicts an effect size. A null result can constrain or reject a specified model only if the design has adequate sensitivity to its prediction. Residuals must also be assessed against conventional systematics and alternative explanations.

## 7. Registry feedback guardrail

Do not mark P2 confirmed or falsified based on an overlap score, band plot, simulated data, or an unplanned residual. Update its status only after a completed, preregistered analysis meets a decision rule tied to a specified model and independently reproducible data.

Any future feedback command is illustrative only and should not be run until the criteria above are frozen. Confirmation, falsification, and undecided outcomes must cite the preregistered result, dataset, and model-specific analysis.

## 8. Readiness gate

P2 remains **planning-stage / blocked for confirmatory testing** until all of the following are available:

- explicit field definitions, units, action, and derived equations;
- an operational Φ proxy and Ω-to-laboratory mapping;
- a derived signed, dimensioned prediction (or justified probability distribution);
- a specified standard-quantum baseline and nuisance/noise model;
- a sensitivity/power calculation and preregistered decision rule;
- a data and analysis provenance plan.

Until these prerequisites are met, any hardware study is exploratory and cannot confirm or falsify P2.

*Document version 1.1 — readiness criteria revised after mathematical specification audit.*
