# Model-closure input record

**Purpose:** collect the minimum explicit inputs needed before deriving a closed Phi-Theory field equation. This is a fill-in record, not a proposed action. Blank or unresolved fields are legitimate outcomes; do not fill them with guessed physics.

**Status:** template only. No new physical assumptions or parameter values are introduced.

## A. Convention freeze

| Item | Author-specified choice | Source / rationale | Status |
|---|---|---|---|
| Spacetime dimension | [fill in] | [reference or rationale] | unresolved |
| Metric signature | [fill in] | [reference or rationale] | unresolved |
| Curvature convention | [fill in] | [reference or rationale] | unresolved |
| Definition of \(\Box\) | [fill in] | [reference or rationale] | unresolved |
| Unit system; treatment of \(c,\hbar\) | [fill in] | [reference or rationale] | unresolved |
| Integration measure and coordinates | [fill in] | [reference or rationale] | unresolved |
| Boundary conditions | [fill in] | [reference or rationale] | unresolved |
| Independent fields varied | [fill in] | [reference or rationale] | unresolved |

## B. Field and function definitions

Complete each row with a mathematical definition, domain, dimensions, parameter values, and provenance. “Named in the equation” is not a definition.

| Symbol | Explicit definition | Dimensions / units | Domain | Parameters and provenance | Status |
|---|---|---|---|---|---|
| \(\Phi\) | [fill in] | [fill in] | [fill in] | [fill in] | unresolved |
| \(V(\Phi)\) | [fill in] | [fill in] | [fill in] | [fill in] | unresolved |
| \(C(\Phi)\) | [fill in] | [fill in] | [fill in] | [fill in] | unresolved |
| \(\Lambda(\Phi)\) | [fill in; state whether related to \(V'\)] | [fill in] | [fill in] | [fill in] | unresolved |
| \(G(\Phi)\) | [fill in] | [fill in] | [fill in] | [fill in] | unresolved |
| \(T(C)_{\mu\nu}\) | [define tensor and its relation to matter fields] | [fill in] | [fill in] | [fill in] | unresolved |
| \(\hat P\) | [define domain, action, and classical/quantum status] | [fill in] | [fill in] | [fill in] | unresolved |
| \(\lambda,\gamma,\eta\) | [define each coupling separately] | [fill in for each] | n/a | [derivation or independent provenance] | unresolved |

## C. Full dynamical specification

Provide the complete action, or explain and justify the alternative dynamical principle. A sectorized expression such as
\[
S=S_{\rm grav}+S_{\Phi}+S_{\rm matter}+S_{\rm additional}
\]
is only an organizational scaffold until every term is written explicitly.

- **Gravitational sector:** [full expression or unresolved]
- **Scalar sector:** [full expression, including all couplings]
- **Matter sector:** [full expression and matter fields]
- **Additional / operator sector:** [full expression or reason absent]
- **Dependence of matter fields on \(\Phi\):** [explicit statement]
- **Parameter provenance:** [source, fit procedure, or derivation for every numerical value]

## D. Derivation record

For each independent field \(q\), attach the variation with enough intermediate steps to check signs, factors, boundary terms, and source conventions.

| Equation | Varied field | Derivation location | Source convention | Dimensional check | Status |
|---|---|---|---|---|---|
| Scalar equation | \(\Phi\) | [file/section or derivation] | [define] | [pass/fail/unresolved] | unresolved |
| Metric equation | \(g_{\mu\nu}\) | [file/section or derivation] | [define stress tensor convention] | [pass/fail/unresolved] | unresolved |
| Matter equations | each \(\psi\) | [file/section or derivation] | [define] | [pass/fail/unresolved] | unresolved |
| Constraints / identities | [identify] | [derivation] | [define] | [pass/fail/unresolved] | unresolved |

The currently displayed scalar-only action, under the assumptions documented in the repository's specification audit, gives
\[
\Box\Phi+V'(\Phi)-\lambda C'(\Phi)=J_m,
\qquad J_m=\frac{1}{\sqrt{-g}}\frac{\delta S_m}{\delta\Phi}.
\]
This conditional result is not a derivation of the separate master-equation ansatz. Do not mark the master equation “derived” until each of its terms is connected to the same complete specification or to a separately justified dynamical rule.

## E. Closure tests

- [ ] All terms in each equation have matching dimensions.
- [ ] The scalar and metric equations are mutually compatible.
- [ ] Stress-energy conservation or its modified form is derived and stated.
- [ ] The roles of \(\Lambda\), \(V'\), the contracted tensor source, \(\gamma C\), and \(\eta\hat P\) are unambiguous.
- [ ] Claimed GR and QM limits follow from explicit limits of the derived equations.
- [ ] The initial/boundary-value problem is specified well enough to calculate a unique result in the stated regime.
- [ ] Numerical parameters have a derivation or independent empirical provenance.

For each unchecked item, record what is missing and who/what can resolve it. Do not replace missing inputs with arbitrary values.

## F. Route to a testable prediction

| Link | Required record | Status |
|---|---|---|
| Field equations → platform dynamics | Explicit Hamiltonian or open-system generator and derivation | unresolved |
| Platform dynamics → observable | Observable, units, estimator, and data-reduction rule | unresolved |
| Model → effect size | Signed effect or distribution with uncertainty | unresolved |
| Baseline → sensitivity | Standard-theory baseline, nuisance/noise model, power/sensitivity analysis | unresolved |
| Test → decision | Preregistered threshold and falsification rule | unresolved |
| Reproduction | Versioned code/data and independent reproduction plan | unresolved |

## Acceptance rule

Until sections A–E are closed, label the master equation **unclosed ansatz**. Until section F is closed, do not present registry values or spectral overlap scores as quantitative laboratory predictions. This template is intended to make missing decisions visible, not to imply that the missing decisions have already been made.

## Related audits

- [Mathematical specification audit](phi_theory_specification_audit.md)
- [Master-equation term closure matrix](master_equation_term_closure.md)
- [Complete-action derivation checklist](complete_action_derivation_checklist.md)
- [Prediction registry audit](prediction_registry_audit.md)
