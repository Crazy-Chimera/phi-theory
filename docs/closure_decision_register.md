# Closure decision register

**Status:** open decision register. This document organizes unresolved author choices; it does not choose conventions, add dynamics, or assert physical validity.

## Purpose and operating rule

Use this register to turn the model-closure input record into a reviewable sequence of decisions. Every decision must be supplied by the theory's author or supported by an explicit derivation/reference. A blank, disputed, or unavailable answer remains **unresolved**. Do not infer a choice merely because one would be conventional.

## Dependency-ordered decisions

| Order | Decision / artifact required | Why it blocks later work | Current disposition | Acceptance evidence |
|---|---|---|---|---|
| 1 | Freeze spacetime dimension, metric signature, curvature convention, definition of `Box`, units, measure, and boundary conditions | Signs, dimensions, and variation depend on these conventions | Unresolved | Completed convention table with source/rationale |
| 2 | Define `Phi`, `V`, `C`, `Lambda`, `G`, `T(C)_{μν}`, `hat P`, and each coupling, including domains and dimensions | Symbols alone do not define a calculable equation | Unresolved | Complete field/function table with parameter provenance |
| 3 | Supply the complete action or a clearly stated alternative dynamical principle | The scalar-only action does not generate all terms in the recorded ansatz | Unresolved | Explicit sectors and statement of independent fields |
| 4 | Derive scalar, metric, and matter equations from that same specification | Prevents mixing terms from unrelated assumptions or conventions | Unresolved | Auditable variations, including signs, boundary terms, and source conventions |
| 5 | Check dimensional consistency, conservation identities, limiting regimes, and well-posedness | Formal equations may otherwise be mutually incompatible or non-predictive | Unresolved | Completed closure tests with pass/fail rationale |
| 6 | Map a closed model to a platform, observable, estimator, effect size, baseline/noise model, and decision rule | A model descriptor is not yet an experimental prediction | Unresolved for P1–P6 | Prediction-specific readiness evidence and preregistration artifact |
| 7 | Reproduce the analysis independently | Establishes that results follow from identified inputs and code | Unresolved | Independent reproduction record with versions and deviations |

## Term-level questions that must not be silently identified

- Is `Lambda(Phi)` defined to equal a derivative of the scalar potential, a combination of derivatives, or something else? State and derive the choice.
- Does the matter action depend explicitly on `Phi`? If yes, calculate its functional derivative; if no, document why the source vanishes.
- Is the contracted tensor source intended to equal the scalar source `J_m`, or is there a separate coupling mechanism? Supply the derivation rather than identifying them by notation.
- What dynamical principle generates `gamma C(Phi)` and `eta hat P(Phi)`? Define the operator, domain, output type, dimensions, and coefficient provenance.
- What metric equation accompanies the scalar equation, and how are conservation identities satisfied?
- What explicit limits are claimed to recover GR, QM, or other regimes, and do those limits follow from the same equations?

Until these are answered, retain the existing classification **unclosed ansatz** for the full master equation. This is a statement about the current record, not a proof that no completion exists.

## Prediction readiness: minimum additional record

For each P1–P6, keep the gate blocked until the evidence identifies all applicable items:

1. Exact model version, assumptions, and parameter provenance.
2. Reproducible derivation from the model to a signed or distributional effect, with units and regime.
3. Operational observable, estimator, sampling/aggregation rule, and laboratory mapping.
4. Baseline/control expectation, alternatives, nuisance variables, and uncertainty model.
5. Feasibility, calibration, sensitivity/power, preregistered decision rule, and falsification criterion.
6. Versioned code/data and a traceable evidence record; independent reproduction when claimed.

For P2 specifically, the current record still needs an operational definition and estimator for (R), a derivation of the effect for a specified platform, an operational mapping for (Omega), a justified target/band fixed before outcomes are seen, and baseline/noise and decision-rule specifications. Do not treat an evidence URL alone as scientific validation.

## Review log

Append one entry per actual decision; do not mark a row complete without its evidence.

| Date | Decision ID | Author-supplied choice or derivation | Evidence / version | Reviewer | Status / unresolved points |
|---|---|---|---|---|---|
| — | — | No closure decisions recorded in this register yet | — | — | Open |

## Related records

- [Model-closure input record](model_closure_input_record.md)
- [Master-equation term closure matrix](master_equation_term_closure.md)
- [Complete-action derivation checklist](complete_action_derivation_checklist.md)
- [Prediction readiness gate](prediction_readiness_gate.md)
- [Conditional dimensional-closure worksheet](conditional_dimensional_closure.md)
