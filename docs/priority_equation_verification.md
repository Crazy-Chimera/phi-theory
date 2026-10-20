# Priority-equation verification audit

**Status:** focused mathematical review of equations already present in the repository. This document does not add physical assumptions, redefine the theory, or claim empirical validation.

## Scope and method

To avoid multiplying the number of formulas that need review, this audit prioritizes four existing items only:

1. the Phi-Theory master-equation ansatz;
2. the scalar action and the equation that follows from varying it;
3. the Omega bridge;
4. the normalized resonance score and its associated kernel/band claims.

The aim is to determine what can be checked from the written mathematics now, what is merely an ansatz, and what evidence is required next. The audit does not treat a formula as verified just because it appears in the registry.

## 1. Master equation — highest priority

The repository records

\[
\Box\Phi+\Lambda(\Phi)
=\frac{8\pi G(\Phi)}{c^4}T(C)_{\mu\nu}g^{\mu\nu}
+\gamma C(\Phi)+\eta\hat P(\Phi).
\]

### Checks that can be made now

- **Algebraic structure:** this is a scalar equation only if every term, including the contracted tensor source, is defined as a scalar.
- **Dimensions:** if coordinates have length units and \([\Box]=L^{-2}\), then every additive term must have units \([\Phi]L^{-2}\). In particular, \(\Lambda\), the tensor-source term, \(\gamma C\), and \(\eta\hat P\) must all match the units of \(\Box\Phi\).
- **Tensor source:** the contraction \(T(C)_{\mu\nu}g^{\mu\nu}\) is formally a scalar, but its physical meaning and normalization are not determined by the notation. It must not be identified with a scalar-field source obtained by variation without a derivation.
- **Variational origin:** the currently displayed scalar action does not derive all of the terms in this equation. The master equation remains an **unclosed ansatz**, not a verified consequence of the action.
- **Metric consistency:** a complete theory must also provide the metric equation and establish compatibility with its stress-energy conservation law or explicitly derived modified identity.

### Minimum evidence needed to close it

A single declared convention sheet; explicit definitions and units for every term; one complete action or a justified alternative dynamical principle; derivations of the scalar and metric equations; and term-by-term dimensional and conservation checks. Do not introduce new terms or parameter values solely to make the equation balance.

## 2. Scalar action — conditional result, not the master equation

The repository currently records

\[
S_\Phi=\int d^4x\sqrt{-g}
\left[
\frac12 g^{\mu\nu}\nabla_\mu\Phi\nabla_\nu\Phi
-V(\Phi)+\lambda C(\Phi)
\right].
\]

With the metric held fixed during scalar variation, vanishing boundary variations, and the source convention
\[
J_m:=\frac{1}{\sqrt{-g}}\frac{\delta S_m}{\delta\Phi},
\]
the displayed action gives the conditional Euler–Lagrange equation
\[
\Box\Phi+V'(\Phi)-\lambda C'(\Phi)=J_m.
\]

This result is a variation of the written scalar sector under those assumptions. It does **not** derive the master equation above: the relationship between \(J_m\) and the contracted tensor source is unspecified, and the origins of the \(\gamma C\) and \(\eta\hat P\) terms are not supplied.

Two further checks are mandatory before treating the action as physically consistent:

- **Kinetic sign:** the signature and action conventions have not been frozen in the original registry. Under the common \((- + + +)\) signature and standard action convention, a healthy real scalar ordinarily has a negative sign in front of \(\tfrac12(\nabla\Phi)^2\). The registry's positive sign therefore requires explicit reconciliation; it should not be silently accepted or silently changed.
- **Action dimensions:** in four dimensions, the Lagrangian density must have dimensions \(L^{-4}\) when coordinates have dimensions of length and the action is dimensionless (natural units). The dimensions of \(\Phi\), any overall normalization, \(V\), \(C\), and \(\lambda\) must be specified together. If \(\Phi\) is dimensionless, the written kinetic term alone has dimensions \(L^{-2}\), so the displayed normalization is not dimensionally complete without additional scale information.

**Disposition:** conditional variational identity recorded; physical sign, normalization, full action, and equivalence to the master equation remain unresolved.

## 3. Omega bridge — units and domain

The repository defines
\[
\Omega=\frac{1}{\Phi}\frac{d\Phi}{dt}.
\]

This is defined only where \(\Phi\ne0\). If \(t\) is ordinary laboratory time, \(\Omega\) has units of inverse time, not automatically a dimensionless value. Any use of \(\Omega\) in a spectral exponent or as an experimental control therefore requires a stated unit convention and an operational definition of \(t\). A reference scale must not be inserted without author approval.

**Disposition:** algebraically recognizable as a logarithmic rate on a domain where \(\Phi\ne0\); operational meaning and units for the repository's proposed use remain unresolved.

## 4. Resonance score — mathematical properties versus physical meaning

The repository defines the normalized overlap
\[
R_\Omega(T_1,T_2)=
\frac{\left|\int S_{T_1}(\omega)S_{T_2}^{*}(\omega)\,d\omega\right|^2}
{\left(\int|S_{T_1}(\omega)|^2\,d\omega\right)
\left(\int|S_{T_2}(\omega)|^2\,d\omega\right)}.
\]

For square-integrable spectra with finite, nonzero norms, the Cauchy–Schwarz inequality gives \(0\le R_\Omega\le1\). This is a mathematical property of the normalized overlap. It does not establish that the score is a probability, a confidence level, or a measured physical effect.

The associated band threshold is a chosen analysis rule, not a physical law unless independently justified. A pointwise kernel defined as a ratio of spectra is undefined where its denominator spectrum is zero; its domain and numerical handling must be explicit. A claim that all theory pairs have resonance one at \(\Phi=1\) does not follow from the overlap definition alone and should remain a separate unverified model assertion unless a proof or construction is supplied.

The spectral transforms also require consistent definitions of their variables and units: the argument of an exponential must be dimensionless, and the integration measures and normalization must be declared.

**Disposition:** normalized-overlap bound is verifiable mathematically under the stated integrability conditions; interpretation as a physical observable and any substrate/universal-resonance claim remain unverified.

## Priority order for further work

Do not expand the formula inventory yet. Resolve these dependencies in order:

1. Freeze signature, curvature convention, \(\Box\), coordinates, units, and field normalization.
2. Check the scalar action's sign and dimensions; state the exact matter-source convention.
3. Define every master-equation term and show its derivation from one common action or explicitly justified alternative principle.
4. Derive the metric equation and check conservation/constraint identities.
5. Only after steps 1–4 pass, connect \(\Phi\) and \(\Omega\) to a specific observable and assess prediction readiness.
6. Separately document the spectral score's input units, normalization, zero-norm/zero-denominator handling, and the distinction between internal software descriptors and empirical measurements.

## Current verdict

| Item | Verdict |
|---|---|
| Master equation | **Unclosed ansatz; not derived from the current action** |
| Scalar Euler–Lagrange equation | **Conditionally derivable from the displayed scalar action** |
| Action sign and dimensional normalization | **Require resolution before physical interpretation** |
| Omega bridge | **Formal rate; units and operational mapping unresolved** |
| Normalized resonance bound | **Mathematically supported under finite, nonzero norm conditions** |
| Universal resonance/substrate claim | **Not implied by the score definition** |
| Empirical predictions | **Not established by these equations alone** |

This audit intentionally prioritizes the few equations with the highest dependency impact rather than adding more speculative formulas. It should be used as a focused review proposal; the model-closure input record and existing draft pull request have not been updated as part of this audit branch.
