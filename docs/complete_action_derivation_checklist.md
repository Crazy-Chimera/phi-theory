# Complete-action and field-equation derivation checklist

**Status:** methodological specification; no new physical terms or parameter values are proposed here.

## Purpose

The current registry contains a Phi-only scalar action and a separate schematic master-equation ansatz. The former does not, by itself, derive every term in the latter. Before numerical predictions or experimental design are attempted, the theory needs one explicit action (or a clearly justified alternative dynamical formulation) from which its equations and observable predictions can be derived.

This checklist is a gate, not a claim that the missing ingredients have known answers.

## 1. Freeze conventions before varying

Record explicitly:

- Spacetime dimension, metric signature, curvature-tensor convention, and definition of \(\Box\).
- Whether units are SI or natural units, and where factors of \(c\) and \(\hbar\) are retained.
- The dimensions, normalization, domain, and allowed boundary conditions of \(\Phi\).
- The integration measure and boundary terms; state which variations vanish at the boundary.
- Whether \(g_{\mu\nu}\), matter fields, and any auxiliary fields are independent variables.

Do not use the same symbol for quantities with different dimensions or meanings.

## 2. Specify the complete dynamical content

Write the full action with separately identified sectors, for example as a *structural placeholder*:

\[
S = S_{\rm grav}[g,\Phi] + S_{\Phi}[g,\Phi]
  + S_{\rm matter}[g,\Phi,\psi] + S_{\rm additional}[g,\Phi,\psi,\ldots].
\]

This expression is only an organizational template, not a proposed Phi-Theory action. For every sector, supply the explicit integrand, fields, functions, parameters, units, and justification. If a term in the master-equation ansatz is intended to arise from an operator, coupling, or matter source, identify its action-level origin. If it is not variational, explain the alternative dynamical principle and its assumptions.

In particular, define rather than merely name:

- \(V(\Phi)\) and \(C(\Phi)\), including their units and parameters;
- the meaning of \(T(C)_{\mu\nu}\), its contraction, and the matter-field dependence on \(\Phi\);
- \(G(\Phi)\), including the gravitational sector in which it appears;
- \(\hat P\), its domain and action, and whether it is a classical operator or a quantum object;
- \(\lambda,\gamma,\eta\), including dimensions, sign conventions, and a derivation or independent empirical basis for each value.

Do not assign numerical values to missing functions or couplings merely to make the equations calculable.

## 3. Derive each equation from the same specification

For each independent field \(q\), show the variation

\[
\delta S = \int d^4x\,\frac{\delta S}{\delta q(x)}\,\delta q(x)
            + \text{boundary terms},
\qquad \frac{\delta S}{\delta q(x)}=0,
\]

with enough intermediate steps to audit signs, factors, and source definitions. Derive the metric equation by varying the metric, the scalar equation by varying \(\Phi\), and matter equations by varying the matter fields. State which equations are independent and identify any constraints or conservation identities.

For the already displayed Phi-only scalar action, under the conventions and assumptions recorded in the specification audit, the scalar equation is

\[
\Box\Phi + V'(\Phi) - \lambda C'(\Phi) = J_m,
\]

where the matter source must be defined consistently from the matter action. This is a conditional result for that action, not a derivation of the full master equation. Additional source terms require additional specified dynamics.

## 4. Run a dimensional and consistency audit

Create a term-by-term table for every equation containing: expression, physical dimensions, units of coefficients, source definition, and derivation location. Verify:

- every term added in an equation has the same dimensions;
- the proposed \(\Omega=\Phi^{-1}d\Phi/dt\) has a declared time variable and units;
- the equations respect the stated symmetries and any required conservation laws;
- the metric and scalar equations are mutually compatible;
- the claimed GR and quantum-mechanical limits follow from explicit limits of the equations, not from narrative assertions;
- the equations are sufficiently specified to calculate a unique result for stated initial/boundary data.

If any check cannot be completed, mark it unresolved and explain why; do not silently repair it with an assumed convention.

## 5. Close the route from equations to an experimental prediction

For each proposed prediction, document this full chain:

1. **Model input:** the exact equation and independently justified parameter values.
2. **Regime:** initial/boundary conditions and domain where the approximation is valid.
3. **Observable map:** an explicit mapping from model fields to a laboratory quantity and estimator.
4. **Calculation:** reproducible derivation or numerical procedure, with units and uncertainty propagation.
5. **Baseline:** standard-theory prediction and nuisance/noise model.
6. **Decision rule:** preregistered effect statistic, uncertainty treatment, sensitivity/power analysis, and falsification criterion.
7. **Provenance:** code, input data, versioned assumptions, and independent reproduction.

An internal spectral overlap score is not a substitute for any of these steps.

## Acceptance gate

The master-equation ansatz should not be described as derived, closed, or quantitatively predictive until each term has a documented origin, the equations pass dimensional and consistency checks, and the observable calculation is reproducible. P1–P6 numerical targets remain provisional until they pass the prediction-specific gate in `prediction_registry_audit.md`. P2 remains blocked from confirmatory testing until its observable, laboratory mapping, derived effect, baseline/noise model, and preregistered decision rule are specified.

## Working record template

Use the [model-closure input record](model_closure_input_record.md) to collect explicit definitions, dimensions, action sectors, derivations, and unresolved closure tests in one fill-in worksheet. It is intentionally a blank template, not a proposed physical model.

## Relationship to other audits

- [Closure decision register](closure_decision_register.md) — dependency-ordered decisions and acceptance evidence for moving from an unclosed ansatz to a derived model.
- [Mathematical specification audit](phi_theory_specification_audit.md)
- [Master-equation term closure matrix](master_equation_term_closure.md)
- [Conditional dimensional-closure worksheet](conditional_dimensional_closure.md)
- [Prediction registry audit](prediction_registry_audit.md)
- [P2 experiment plan](experiment_P2_mesoscopic.md)
- [Experimental roadmap](experimental_roadmap.md)
