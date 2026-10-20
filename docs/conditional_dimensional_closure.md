# Conditional dimensional-closure worksheet

**Status:** symbolic consistency constraints only. This worksheet does not assign dimensions to `Phi`, choose units, or supply missing model definitions. The constraints below are conditional on the conventions stated in each section.

## 1. Master equation: general constraint

The recorded ansatz is

\[
\Box\Phi+\Lambda(\Phi)=\frac{8\pi G(\Phi)}{c^4}T(C)_{\mu\nu}g^{\mu\nu}
+\gamma C(\Phi)+\eta\hat P(\Phi).
\]

Let \([\Phi]=F\), and let the coordinates and metric convention make \([\Box]=L^{-2}\). Then dimensional consistency requires every additive term to have dimensions \(F L^{-2}\):

| Expression | Required dimensions | Still needed |
|---|---|---|
| \(\Box\Phi\) | \(F L^{-2}\) under this convention | Definition of \(\Box\), coordinates, and field normalization |
| \(\Lambda(\Phi)\) | \(F L^{-2}\) | Explicit function and units |
| \(\frac{8\pi G(\Phi)}{c^4}T(C)_{\mu\nu}g^{\mu\nu}\) | \(F L^{-2}\) | Definition and dimensions of \(G(\Phi)\), tensor source, contraction, and normalization |
| \(\gamma C(\Phi)\) | \(F L^{-2}\) | Dimensions of \(C\) and \(\gamma\) |
| \(\eta\hat P(\Phi)\) | \(F L^{-2}\) | Output dimensions of \(\hat P\) and dimensions of \(\eta\) |

These are compatibility requirements, not evidence that the terms have been correctly defined or derived.

## 2. Displayed scalar action: conditional constraint

For the displayed expression

\[
S_\Phi=\int d^4x\sqrt{-g}\left[\tfrac12 g^{\mu\nu}\nabla_\mu\Phi\nabla_\nu\Phi-V(\Phi)+\lambda C(\Phi)\right],
\]

suppose coordinates have dimensions of length, \(g^{\mu\nu}\) is dimensionless, and derivatives have dimensions \(L^{-1}\). The three terms inside the brackets must then share dimensions:

\[
[V]=[\lambda C]=[\Phi]^2 L^{-2}.
\]

This comparison assumes the written kinetic normalization is used directly. If an omitted overall dimensional prefactor, nonstandard field normalization, or different coordinate convention is intended, the dimensions must be recalculated from the complete action. In particular, this worksheet does not determine \([\Phi]\), \([V]\), \([C]\), or \([\lambda]\) separately.

The conditional Euler–Lagrange result remains

\[
\Box\Phi+V'(\Phi)-\lambda C'(\Phi)=J_m,
\]

so \([V']=[\lambda C']=[J_m]=F L^{-2}\) under the same assumptions. This does not establish an identification with the separate master-equation terms.

## 3. SI stress-energy check (explicitly conditional)

If, and only if, \(T(C)_{\mu\nu}g^{\mu\nu}\) is a contraction with the ordinary SI stress-energy tensor (energy density units \(\mathrm{J\,m^{-3}}\)) and \(G(\Phi)\) has the SI units of Newton's gravitational constant, then

\[
\left[\frac{G}{c^4}T_{\mu\nu}g^{\mu\nu}\right]=L^{-2}.
\]

That factor alone has curvature dimensions, not automatically the dimensions \(F L^{-2}\) required by the equation above. The field-dependent coupling or source normalization would have to supply the remaining factor of \(F\), or the equation's field/source conventions would need to be specified differently. Do not assume this ordinary stress-energy interpretation for the notation \(T(C)_{\mu\nu}\) until it is defined.

## 4. Omega bridge

For \(\Omega=\Phi^{-1}d\Phi/dt\), provided \(\Phi\ne0\) and \(t\) is laboratory time,

\[
[\Omega]=T^{-1}.
\]

A dimensionless interpretation requires an explicitly specified reference time or a different definition. No reference time is selected here.

## 5. Closure record

Do not mark dimensional closure as passed until the model author records the convention choices and explicit definitions in [the model-closure input record](model_closure_input_record.md), then checks every term using those choices.

| Check | Status |
|---|---|
| Field normalization and unit system fixed | unresolved |
| Dimensions of every action term and any overall prefactor recorded | unresolved |
| Dimensions of each master-equation term match | unresolved |
| Tensor source and gravitational coupling defined consistently | unresolved |
| Dimensions and operational time variable for \(\Omega\) fixed | unresolved |

**Conclusion:** the current text supports conditional dimensional constraints, but not a completed dimensional audit. No physical parameters or missing definitions have been inferred.
