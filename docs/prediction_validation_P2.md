# P2 — Quantitative validation worksheet (preregistration draft)

**Status: BLOCKED pending model specification. This document is a planning worksheet, not an experimental result or a validated prediction.**

P2 proposes looking for a deviation from standard quantum-mechanical dynamics in mesoscopic systems. The current registry records a target scale of `ΔR = 0.05`, and the experiment outline suggests quantum dots or circuit-QED platforms. Those entries do not yet define a reproducible, dimensioned prediction: the symbol `R` is not operationally specified for an experiment, and the mapping from the model's dimensionless `Ω` coordinate to a controlled or measured laboratory quantity is not supplied.

Do not label P2 “confirmed” or “falsified” on the basis of the registry resonance score, a band plot, a simulation generated from qualitative spectra, or a post-hoc residual alone.

## 1. Freeze the model before collecting outcome data

Complete and version the following fields before unblinding or analysing the confirmatory dataset:

| Required item | Must be recorded | Current status |
|---|---|---|
| Primary observable | One measurable quantity, units, estimator, and data-reduction code | Missing |
| Ω-to-laboratory mapping | Equation mapping Ω to a physical/control variable, including units and parameter values | Missing |
| Φ operationalization | A defined measurable proxy or independently estimated quantity, with uncertainty | Missing |
| Prediction equation | Derivation from the stated model, including all free parameters and assumptions | Missing |
| Expected effect | Signed effect size or a probability distribution, with units and uncertainty | Not established by the current `ΔR` entry |
| Resonant interval | A rule that maps the model's band endpoints to the laboratory domain before seeing results | Missing |
| Standard-model baseline | Preselected Schrödinger/Lindblad model, nuisance parameters, and model-selection procedure | Incomplete |
| Confounders | Platform-specific noise sources, drift, calibration, selection effects, and mitigation plan | Missing |
| Statistical plan | Primary endpoint, sample-size/power calculation, exclusion rules, multiplicity correction, and decision threshold | Missing |
| Falsification rule | A quantitative rule that can reject the specified alternative, including sensitivity requirements | Incomplete |
| Data provenance | Public dataset or acquisition protocol, instrument metadata, and immutable analysis version | Missing |

A field should not be filled with a convenient number merely to make the table complete. If the model cannot provide a mapping or derive an effect size, record that limitation and keep the prediction untested.

## 2. Minimum experiment record

For each run, preserve:

- protocol and preregistration version;
- device/platform identity and calibration records;
- raw data or a durable repository link, subject to legitimate privacy/security constraints;
- environmental and control-variable metadata;
- preprocessing and exclusion decisions, made without access to the confirmatory outcome where practical;
- standard-quantum-model fit, residuals, uncertainty estimates, and diagnostics;
- the prespecified Φ proxy and its uncertainty;
- exact software commit, dependencies, and command used for analysis.

Report null, positive, and inconclusive outcomes. “No statistically significant effect” is not by itself evidence of falsification unless the study had the preregistered sensitivity to exclude the model's predicted effect.

## 3. Analysis sequence

1. **Model freeze:** resolve every blocking field in Section 1 and publish the equations and analysis plan.
2. **Validation data:** test the fitting and residual pipeline on simulated data with known injected effects and on null data. Label these as software validation, not physical evidence.
3. **Pilot:** estimate instrument noise and nuisance parameters. Keep pilot data separate from the confirmatory test, or document any changes and preregister a new confirmatory analysis.
4. **Confirmatory run:** follow the frozen protocol and retain raw data and metadata.
5. **Independent reproduction:** have another analyst reproduce the reported primary result from the retained data and frozen code.
6. **Registry update:** change the prediction status only after the decision rule is met and cite the dataset, analysis version, and uncertainty. Otherwise retain `undecided` or `untested`.

## 4. Guardrails on interpretation

- The repository's spectral overlap value (currently listed as approximately 0.518 for P2) is a model-internal score computed from the project's spectrum descriptors; it is not an experimental probability, confidence level, or predicted effect size.
- The listed `ΔR = 0.05` is not yet a reproducible physical prediction until `R`, its units/estimator, and its derivation are specified.
- A band in the Ω coordinate is not experimentally actionable until the Ω-to-laboratory mapping is stated independently of the observed outcome.
- A residual from a standard quantum model is not evidence for a new effect unless known systematics and alternative conventional explanations have been addressed.
- This worksheet does not assert that the proposed effect exists. It is designed to make the claim testable or to identify precisely why it is not yet testable.

## 5. Ready-to-test gate

P2 should be marked **ready for confirmatory testing** only when all Section 1 fields are complete, the equations and code are versioned, the sample-size/sensitivity justification is documented, and the decision rule is fixed before confirmatory outcomes are inspected.
