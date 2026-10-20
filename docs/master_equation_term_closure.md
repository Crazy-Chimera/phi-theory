# Master-equation term closure matrix

**Status:** equation-level audit of the current registry. This document does not supply missing physics or infer new parameter values.

## Purpose

The registry records a schematic master equation,

\[
\Box\Phi+\Lambda(\Phi)=\frac{8\pi G(\Phi)}{c^4}T(C)_{\mu\nu}g^{\mu\nu}
+\gamma C(\Phi)+\eta\hat P(\Phi),
\]

alongside a Phi-only scalar action. The matrix below distinguishes terms that are named in the ansatz from terms that have an identified derivation in the displayed action. A symbolic name is not, by itself, a definition or derivation.

## Term-by-term status

| Term or structure | What is currently recorded | What is still needed before derivation or calculation |
|---|---|---|
| \(\Box\Phi\) | Kinetic operator appears in the scalar equation and ansatz | Metric signature, definition of \(\Box\), units, field normalization, and boundary assumptions |
| \(\Lambda(\Phi)\) | Appears in the master-equation left-hand side | Explicit definition and relation, if any, to \(V'(\Phi)\) or another action term |
| \(G(\Phi)\) | Variable gravitational coupling appears on the right-hand side | Explicit function, units, gravitational action, constraints, and variation that produces the proposed coupling |
| \(T(C)_{\mu\nu}g^{\mu\nu}\) | A contracted tensor source is written | Definition of \(T(C)_{\mu\nu}\), its relation to a matter stress tensor, the meaning of its dependence on \(C\), and how its scalar source follows from variation |
| \(\gamma C(\Phi)\) | A term is named and a numerical coefficient is listed | Definition and dimensions of \(C\), dimensions and independent basis for \(\gamma\), and an action-level origin or explicitly non-variational rule |
| \(\eta\hat P(\Phi)\) | An operator term is named and a numerical coefficient is listed | Definition/domain of \(\hat P\), its output and dimensions, status as classical or quantum, dimensions and basis for \(\eta\), and a derivation |
| \(V(\Phi)\) | Potential appears in the displayed Phi-only action | Explicit potential and parameters; its derivative contributes \(V'(\Phi)\) to the scalar equation under the stated convention |
| \(\lambda C(\Phi)\) | Coupling appears in the displayed Phi-only action | Explicit \(C\), units of \(\lambda\), and a consistent convention; variation contributes \(-\lambda C'(\Phi)\) to the displayed scalar equation |
| Matter source \(J_m\) | Can be defined from a specified matter action | State the functional-derivative measure and sign convention; with \(J_m=(1/\sqrt{-g})\,\delta S_m/\delta\Phi\), the source appears on the right-hand side of the stated scalar equation |

## What follows from the displayed action

For the currently displayed scalar action, with the metric treated as fixed during scalar variation, vanishing boundary variations, and the stated source convention, the scalar equation is

\[
\Box\Phi+V'(\Phi)-\lambda C'(\Phi)=J_m,
\qquad
J_m:=\frac{1}{\sqrt{-g}}\frac{\delta S_m}{\delta\Phi}.
\]

The equation is conditional on the declared metric/kinetic convention and on a specified matter action. If no matter action depends on \(\Phi\), then \(J_m=0\). If it does depend on \(\Phi\), its functional derivative must be calculated from that explicit dependence.

This variation does not derive the complete master-equation ansatz as currently written. In particular, the displayed scalar action alone does not establish the tensor-source term, the \(\gamma C\) term, or the \(\eta\hat P\) term. Their absence from this derivation is not proof that such terms are impossible; it means the present specification has not derived them.

## Required closure record

For every proposed master-equation term, add a record containing:

1. its exact mathematical definition and dimensions;
2. the action term or alternative dynamical postulate from which it follows;
3. the variation or derivation, including sign and normalization;
4. its independent parameter values and provenance;
5. compatibility with the metric equation, conservation laws, and stated limiting regimes;
6. the reproducible calculation connecting it to an observable.

If any item is unavailable, mark that term **unclosed** rather than supplying a guessed expression.

## Related documents

- [Mathematical specification audit](phi_theory_specification_audit.md)
- [Complete-action derivation checklist](complete_action_derivation_checklist.md)
- [Prediction registry audit](prediction_registry_audit.md)
- [Experimental roadmap](experimental_roadmap.md)
