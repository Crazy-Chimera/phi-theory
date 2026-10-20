# Ω-RE equation testing record

**Scope:** focused verification of equations already recorded in the repository. This record does not add physical terms, choose missing model conventions, or treat spectral similarity as physical validation.

**Working rule:** Ω-RE is used in two distinct layers: (1) mathematical/specification checks on the model equations and (2) numerical tests of the implemented spectral pipeline. A pass in layer 2 cannot close an unresolved equation in layer 1.

## 1. Priority order

Keep the verification set deliberately small and dependency-ordered:

1. **Master equation** — check whether each term is defined, dimensionally comparable, and derived from the same action or an explicitly stated alternative dynamical principle.
2. **Scalar-action equation** — verify the conditional Euler–Lagrange result from the displayed scalar action, keeping its source convention and assumptions explicit.
3. **Ω bridge** — check domain and units, and require an operational definition before connecting it to a laboratory control or measurement.
4. **Normalized resonance score** — test mathematical invariants and numerical edge cases in the implementation.
5. **Band/kernel outputs** — verify their software properties while keeping them distinct from a derivation of physical emergence.

Do not introduce additional candidate equations until these checks identify a specific dependency that must be resolved.

## 2. Equation-level results

| Target | Ω-RE check | Result | What would change the status |
|---|---|---|---|
| Master equation, as recorded in README and the registry | Term definitions, units, and derivation from the displayed action | **Unclosed ansatz; not derived by the displayed scalar action** | Complete dynamical specification; explicit definitions and dimensions for every term; auditable variation or other justified derivation; compatible metric equation and conservation checks |
| Scalar equation from the displayed scalar action | Conditional variation with fixed metric, vanishing boundary variations, and the repository's stated source convention | **Conditionally identified** as `Box Phi + V'(Phi) - lambda C'(Phi) = J_m` | Freeze metric/`Box` and kinetic-sign conventions; provide explicit matter action and verify the variation end-to-end |
| `Omega = (1/Phi) dPhi/dt` | Domain and dimensional check | **Formal check only**: requires `Phi != 0`; if `t` is laboratory time, its units are inverse time | Define the time parameter, field normalization, and operational measurement/control mapping |
| Normalized spectral resonance | Cauchy–Schwarz bound and numerical implementation behavior | **Mathematical invariant is testable** for finite, nonzero spectra on a valid integration grid; the score is not a probability or empirical effect | Preserve unit/property tests; define the spectral measure and sampling/interpolation assumptions for each intended use |
| Bands and kernel | Verify implementation contracts and interpretation boundaries | **Software descriptors only**; local overlap bands and the regularized ratio kernel do not establish a physical derivation | Document grid/threshold choices and demonstrate that a kernel maps one specified equation into another while preserving units and assumptions |

The detailed equation closure and derivation prerequisites remain in `docs/master_equation_term_closure.md`, `docs/complete_action_derivation_checklist.md`, and `docs/phi_theory_specification_audit.md`. This record does not replace or modify those records.

## 3. Ω-RE Testing Assistant: software verification checklist

Run from the repository root:

```bash
python tests/test_pipeline.py
python omega_re.py protocol
python omega_re.py resonance "Phi-Theory" "Quantum Mechanics"
python omega_re.py bands "Phi-Theory" "Quantum Mechanics"
```

The theory names supplied to the CLI must match the names in `registry/theories.yaml`; if the example labels do not match, use the registered names shown by `python omega_re.py list-theories -v`.

Minimum assertions for the implemented resonance score:

- identical nonzero spectra yield a score numerically close to 1;
- scores are finite and within [0, 1] for valid finite inputs;
- a zero-norm spectrum returns the documented safe fallback, not NaN;
- non-finite inputs, mismatched lengths, and invalid grids are rejected;
- nonuniform grids are integrated using their actual coordinate values;
- the band profile is explicitly identified as a peak-normalized local descriptor, not the global integrated score;
- dry-run feedback does not mutate prediction or resonance files.

These assertions are represented in the existing `tests/test_pipeline.py`. The last observed GitHub Actions result on the base branch was **success** for commit `d1eb213154e11581d716d6e05c3dc9452accfe4d`; that result is baseline evidence only, not a test run of this new record/branch.

## 4. Stop/go rules

- **GO for software-level checks:** numerical invariants, validation behavior, CLI consistency, and dry-run safety can be tested with synthetic fixtures.
- **STOP for physical confirmation:** do not mark the master equation as verified, claim an emergent derivation, or promote P1–P6 to confirmed on the basis of synthetic spectra, resonance scores, band thresholds, or a passing software test suite.
- **STOP for quantitative prediction:** the master equation remains blocked until the term-closure and prediction-readiness requirements are met.
- **No silent repair:** unresolved definitions, units, signs, coefficients, and operator domains stay unresolved rather than being filled with conventional or guessed values.

## 5. Current disposition

This is a focused test record, not a new physical model. The highest-priority finding is that the software can test its resonance arithmetic, while the recorded master equation cannot yet be confirmed from the current action specification. The next meaningful model-level test depends on author-supplied closure inputs; it cannot be manufactured by increasing the number of formulas or by assigning an Ω-RE score to the equation.
