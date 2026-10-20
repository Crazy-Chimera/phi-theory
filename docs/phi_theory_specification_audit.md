# Phi-Theory mathematical specification audit (P2 readiness)

**Status: audit of the repository's written equations; not a derivation of new physics.** This note identifies what follows from the current text and what remains unspecified. It does not establish that Phi-Theory is empirically valid.

## Executive finding

The current registry does not yet define a closed, quantitatively predictive model for a mesoscopic quantum experiment. The listed action and master equation are schematic: essential functions, couplings, field definitions, and links to laboratory observables are missing. Therefore the registry value \(\Delta R=0.05\), the P2 band endpoints, and the spectral overlap score cannot currently be derived as an experimental effect prediction from the displayed equations.

## 1. Equations currently recorded

The registry gives, in schematic notation,

\[
S[\Phi]=\int d^4x\sqrt{-g}\left[\tfrac12 g^{\mu\nu}\nabla_\mu\Phi\nabla_\nu\Phi - V(\Phi)+\lambda C(\Phi)\right],
\]

and a master equation of the form

\[
\Box\Phi+\Lambda(\Phi)=\frac{8\pi G(\Phi)}{c^4}T(C)_{\mu\nu}g^{\mu\nu}
+\gamma C(\Phi)+\eta\hat P(\Phi).
\]

It also defines

\[
\Omega=\frac{1}{\Phi}\frac{d\Phi}{dt}.
\]

These are not yet a single fully specified dynamical system: the relationship between the action and the master equation is not shown, and several terms are undefined.

## 2. Missing specifications

| Item | What must be specified | Why it matters |
|---|---|---|
| Field and units | Whether \(\Phi\) is dimensionless or dimensionful; normalization and domain | Determines units of every term and whether the equations are dimensionally consistent |
| Metric/sign conventions | Metric signature, definition of \(\Box\), units and coordinate conventions | Needed to interpret the kinetic term and derive the field equation |
| Potential | Explicit \(V(\Phi)\) and its parameters | A symbolic name alone does not determine dynamics |
| Coupling function | Explicit \(C(\Phi)\), including units and parameters | Its variation and coupling to matter are unspecified |
| Matter coupling | Definition of \(T(C)_{\mu\nu}\), its trace/contraction, and how matter fields depend on \(\Phi\) | Needed to calculate a source for \(\Phi\) |
| Variable gravitational coupling | Form and constraints on \(G(\Phi)\) | Needed to make quantitative predictions and check existing bounds |
| Operator term | Definition, domain, and action of \(\hat P\); whether it is classical or quantum | The equation is not calculable until this term is defined |
| Coefficients | Units, signs, physical meaning, and independently justified values for \(\lambda,\gamma,\eta\) | Values such as \(10^{-30}\) are not interpretable without a unit convention and derivation |
| Quantum dynamics | A specified Hamiltonian or master equation for a chosen platform | No correction to Schrödinger/Lindblad evolution can currently be computed |
| Observable map | Equation from \(\Phi\) or \(\Omega\) to a measured quantity and estimator | Required to turn the framework into a falsifiable laboratory prediction |

## 3. Dimensional check on the Omega bridge

If \(t\) is ordinary laboratory time, then

\[
[\Omega]=[\Phi^{-1}][d\Phi/dt]=\mathrm{time}^{-1}
\]

provided \(\Phi\ne0\). Thus \(\Omega\) has units of inverse time, not a dimensionless unit, under that interpretation. It could be made dimensionless by introducing a specified reference time, for example \(\tilde\Omega=\tau_0\,d\ln|\Phi|/dt\), but choosing \(\tau_0\) would be an additional model decision and must not be silently assumed. If \(t\) is not laboratory time, its operational meaning must be defined instead.

The recorded P2 interval \([3.39\times10^{-5},0.216]\) therefore has no usable laboratory interpretation until the units of \(\Omega\), its time variable, and the mapping to experimental controls are fixed.

## 4. What can and cannot be derived now

**Can be stated from the repository:** the symbolic ansatz for an action, a schematic master equation, a proposed logarithmic rate \(\Phi^{-1}d\Phi/dt\), and heuristic spectra used by the software to calculate internal overlap scores.

**Cannot be derived from the repository as currently specified:** a unique correction to a quantum-dot Hamiltonian or Lindblad generator; a numerical shift in interference visibility, level spacing, or decoherence rate; a justified \(\Delta R=0.05\); a mapping from the listed band endpoints to experimental settings; or a power/falsification threshold tied to a model-predicted effect.

The numerical spectral descriptors in the registry are qualitative presets. Computing a reproducible overlap from them establishes a property of those chosen descriptors, not an independent physical consequence of the field equations.

## 5. Minimum route to a testable P2 model

1. Define \(\Phi\), its units, and how it can be independently estimated in the proposed platform.
2. Choose consistent conventions and fully specify the action, all functions, couplings, operators, and parameters.
3. Derive the field equation by variation and demonstrate that it agrees with the intended master equation, including matter coupling.
4. Specify the standard quantum model for one platform and derive exactly how \(\Phi\) modifies its Hamiltonian or open-system generator.
5. Derive a signed prediction for one primary observable, including parameter uncertainty and units.
6. Define the \(\Omega\)-to-control mapping and show how the proposed band is selected before observing outcomes.
7. Only then set noise assumptions, power, exclusions, multiplicity handling, and a preregistered decision rule.

If the model cannot provide these details, the correct status remains **blocked / untested**. Do not assign arbitrary parameter values merely to produce a numerical forecast.

## Scope note

This is a specification audit based on the equations currently stored in the repository. It is not an external peer review, a proof of inconsistency, or evidence for or against the existence of a new physical effect.


## 6. Variational check of the displayed action

For the displayed scalar-field part
\[
S_\Phi=\int d^4x\sqrt{-g}\left[\tfrac12 g^{\mu\nu}\nabla_\mu\Phi\nabla_\nu\Phi - V(\Phi)+\lambda C(\Phi)\right],
\]
assume the metric is fixed during this variation, the boundary term vanishes, and any matter action is denoted by \(S_m\). Define its scalar source by
\[
J_m(x):=\frac{1}{\sqrt{-g}}\frac{\delta S_m}{\delta\Phi(x)}.
\]
The Euler–Lagrange equation from this action and source is then
\[
\Box\Phi+V'(\Phi)-\lambda C'(\Phi)=J_m.
\]
This is the equation implied by the written action under those assumptions. The overall sign of the kinetic term and the interpretation of \(\Box\) must be reconciled with an explicitly declared metric signature and convention.

**Comparison with the recorded master-equation ansatz:** the ansatz contains \(\Lambda(\Phi)\), a contracted \(T(C)_{\mu\nu}g^{\mu\nu}\) term multiplied by \(G(\Phi)\), and the terms \(\gamma C(\Phi)\) and \(\eta\hat P(\Phi)\). These do not follow from the displayed scalar action as written. They could be included only after the model specifies their definitions and units and supplies an action or other justified dynamical principle whose variation produces them. In particular, the matter source from a scalar-dependent matter action is not automatically equivalent to the displayed gravitational trace term. The two equations therefore must not be presented as equivalent at this stage.

This check does **not** prove the broader theory inconsistent; it establishes only that the currently documented action is insufficient to derive the current master-equation ansatz. The registry now distinguishes the variational equation from the unclosed ansatz. No arbitrary replacement values or new physical terms have been introduced.

## 7. Required next derivation

Before claiming a corrected, closed master equation, specify: (1) metric signature and units; (2) the full action including gravity and matter; (3) the functional dependence of matter fields on \(\Phi\); (4) explicit \(V,C,G,\Lambda\) and operator \(\hat P\); and (5) the dimensions and independent justification of every coupling. Then vary the full action with respect to both \(\Phi\) and the metric, derive the corresponding field equations, and check each term's dimensions. Until this is done, the registry's master equation is an ansatz, not a verified consequence of the action.
