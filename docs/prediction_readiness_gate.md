# Prediction readiness gate (P1–P6)

**Purpose:** apply one consistent, evidence-based gate before any prediction is described as quantitatively derived or used to justify confirmatory testing. This is a project-management checklist, not a source of missing physics. The gate does not assign new target values, select parameters, or establish that Phi-Theory is valid.

## Gate states

Use these states separately:

- **Blocked:** at least one prerequisite needed to define or derive the prediction is absent.
- **Ready for design review:** the derivation and observable are specified well enough to assess feasibility and design a preregistration; no empirical conclusion is implied.
- **Preregistered:** protocol, primary outcome, exclusions, uncertainty treatment, and decision rule were frozen before confirmatory data collection.
- **Tested:** data were collected and analyzed under the frozen protocol; report the outcome and deviations without equating a workflow label with scientific truth.
- **Independently reproduced:** an independent analysis reproduces the reported result from identified inputs and code.

Do not skip a state by changing a registry label. A status transition requires a cited evidence record and review against the applicable criteria below.

## Universal acceptance criteria

A prediction cannot pass the derivation/readiness gate until all applicable items are recorded:

1. **Model source:** exact equation(s), versioned assumptions, and parameter values with provenance.
2. **Derivation:** reproducible algebra or numerical method connecting the model to the target, with units and approximation regime.
3. **Operational observable:** named measured quantity, estimator, units, sampling/aggregation rule, and how it is obtained.
4. **Baseline and alternatives:** standard-model or control expectation, nuisance variables, and a defined competing hypothesis.
5. **Uncertainty:** parameter, measurement, and model uncertainty treatment; noise/covariance assumptions where relevant.
6. **Decision rule:** primary statistic, direction or interval of the predicted effect, exclusion/multiplicity handling, sensitivity or power justification, and falsification criterion.
7. **Feasibility and provenance:** suitable data/platform, calibration, analysis code, versioned inputs, and a traceable evidence record.

If a criterion is not applicable, explain why. If it is unknown, mark it unresolved; do not silently substitute a default. A qualitative descriptor or nonempty evidence-reference string does not satisfy any scientific criterion by itself.

## Prediction-specific gate

| ID | Current gate | Prediction-specific evidence required to advance |
|---|---|---|
| **P1 — Phi-Theory/LQG** | **Blocked** | Define a shared operational observable between the two frameworks; specify the consistent model and regime; derive the stored deviation target (or replace it only through a documented model revision); identify the dataset/data-generation procedure, uncertainty model, and decision rule. |
| **P2 — mesoscopic quantum dynamics** | **Blocked; no confirmatory testing** | Define (R) and its estimator; derive the effect from a closed model for a specified platform; operationalize (Omega) and its mapping to experimental controls; justify the target and band before outcomes are seen; specify baseline/noise, calibration, power/sensitivity, preregistration, and falsification rule. See `prediction_validation_P2.md` and `experiment_P2_mesoscopic.md`. |
| **P3 — Yukawa/Standard Model** | **Blocked** | Specify the explicit (Phi)-matter interaction and its independent parameter basis; derive a measurable Yukawa-related shift with units and regime; reconcile the target with existing constraints; define observable, uncertainty, and a feasible analysis. |
| **P4 — QED / fine-structure constant** | **Blocked** | Derive the (Phi)-dependent correction to (alpha) or the chosen QED observable; state scale/environment dependence and units; document independent bounds and calibration; show the proposed target and threshold are distinguishable from uncertainty and systematic effects. |
| **P5 — gravity / (G)** | **Blocked** | Supply a complete gravity-plus-scalar action or justified alternative; derive field equations and the form/constraints of (G(Phi)); define the measurable (Phi) proxy and experimental observable; derive the target and decision rule under a stated regime. |
| **P6 — classical/quantum boundary** | **Blocked** | Operationally define (S) and the platform; derive a quantitative model contrast rather than infer an effect from a zero overlap score; specify the standard baseline, nuisance/noise model, joint-analysis plan, and falsifiable decision rule. |

The labels above reflect missing prerequisites in the repository's current specification, not a claim that the hypotheses are false or permanently untestable. Current numerical targets and (R_\Omega) scores remain provisional until a derivation and evidence chain are supplied.

## Evidence record template

For each attempted gate transition, record:

- Prediction ID and registry version:
- Gate being requested:
- Model/action and equation references:
- Derivation or calculation artifact (version/hash):
- Observable and estimator:
- Target/effect and units, including uncertainty:
- Baseline, nuisance/noise model, and data source:
- Preregistered decision rule / falsification criterion:
- Evidence references and what each one actually supports:
- Reviewer and review date:
- Unresolved items and deviations:

An evidence reference must identify the material and its role; merely supplying a URL or path is not validation. A reviewer should be able to distinguish evidence for software behavior, mathematical derivation, feasibility, and empirical outcomes.

## Relationship to existing records

- `prediction_registry_audit.md` records the current entry-by-entry scientific limitations and the semantics of registry fields.
- `phi_theory_specification_audit.md` records the current equation-level gaps and the conditional variation of the displayed scalar action.
- `master_equation_term_closure.md` identifies the missing definition or derivation for each term.
- `complete_action_derivation_checklist.md` provides the full-action derivation workflow.
- `experimental_roadmap.md` records provisional candidate platforms and ordering; internal spectral scores do not establish experimental priority.

**Acceptance rule:** until the relevant prediction-specific requirements and the universal criteria are supported by reviewable artifacts, keep the prediction blocked for confirmatory use.