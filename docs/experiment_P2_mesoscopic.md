# Experiment P2 — Mesoscopic Resonance (Phi-Theory ↔ Quantum Mechanics)

| | |
|---|---|
| **Prediction ID** | P2 |
| **Pair** | Phi-Theory ↔ Quantum Mechanics |
| **Spectral R_Ω** | ≈ 0.518 |
| **Band** | Ω ∈ [3.39×10⁻⁵, 0.216], center ≈ 2.71×10⁻³ |
| **Observable** | ΔR (mesoscopic) — deviation from pure Schrödinger evolution |
| **Status** | undecided (planning stage; confirmatory test blocked) |
| **Priority** | #2 overall; #1 among near-term lab tests |

---

## 1. Scientific goal

Test whether systems in the **mesoscopic regime** (roughly 10–1000 atoms / artificial atoms) show systematic deviations from standard quantum mechanics that correlate with the Ω-resonant band between Phi-Theory and QM.

Phi-Theory treats entanglement density Φ as fundamental. In the mesoscopic window the classical–quantum transition is incomplete; Ω-RE predicts a **resonant band** where emergence is strongest and small Φ-dependent corrections become visible.

---

## 2. Target systems

| Platform | Why suitable | Typical N |
|----------|--------------|-----------|
| Semiconductor quantum dots | Tunable confinement, optical & transport readout | 1–100 electrons |
| Superconducting circuits (transmons / resonators) | High coherence, circuit QED toolbox | effective mesoscopic |
| Trapped-ion crystals (small) | Individual control, entanglement engineering | 10–100 ions |
| Molecular magnets / spin clusters | Intrinsic mesoscopic spin | 10–1000 spins |
| Nanomechanical resonators | Classical↔quantum boundary in mechanics | 10⁶–10⁹ atoms (mass) |

**Primary recommendation:** gate-defined GaAs or Si/SiGe quantum dots + circuit QED resonators.

---

## 3. Observable and null hypothesis

**Null (standard QM):** Dynamics fully described by Schrödinger / Lindblad evolution with environment-independent constants.

**Alternative (Phi / Ω-RE; not yet quantitatively specified):** The framework proposes a possible systematic residual inside a resonant Ω band, correlated with a proxy for local Φ. The repository does not yet derive a unique observable or quantitative laboratory prediction from this proposal.

$\Delta R = (R_{obs} - R_{QM}) / R_{QM}$

This expression is only a placeholder until the experimental meaning of $R_{obs}$ and $R_{QM}$, their estimator, units, and uncertainty are defined. The registry target $\Delta R \sim 0.05$ is currently unsupported by a derivation and must not be treated as a measured or model-derived effect size. The mapping from $\Omega$ to controllable laboratory variables is also missing. P2 is therefore **not ready for confirmatory testing**. See [`prediction_validation_P2.md`](prediction_validation_P2.md).

---

## 4. Measurement protocol (outline)

1. Prepare mesoscopic states with controlled entanglement.
2. Evolve under characterised Hamiltonian spanning the Ω band.
3. Read out interference / spectroscopy / transport.
4. Compare residuals vs best standard QM + noise model.
5. Correlate residuals with Φ-proxy (multipartite entanglement, circuit depth).
6. Optional: high-Φ vs low-Φ environments.

---

## 5. Required sensitivity

| Item | Target |
|------|--------|
| Statistical precision on ΔR | ≤ 0.01 (ideally 0.001) |
| Noise control | state of the art for platform |
| Ω ↔ experiment mapping | documented model |

---

## 6. Falsification

No systematic deviation inside the resonant band at target sensitivity, or deviations fully explained by standard noise without Φ correlation.

---

## 7. Feedback into Ω-RE

```bash
python omega_re.py feedback P2 confirmed --note "mesoscopic ΔR detected"
python omega_re.py feedback P2 falsified --note "null result"
python omega_re.py feedback P2 undecided --note "systematics limited"
```

---

## 8. Exploratory work only (timeline conditional on model completion)

1. Specify and justify a measurable Φ proxy and the Ω-to-laboratory mapping.
2. Derive a signed, dimensioned effect prediction (or a justified distribution) from the model.
3. Define the standard-QM baseline, nuisance/noise model, power calculation, and preregistered decision rule.
4. Only then choose a platform and run pilot/confirmatory measurements. Until those prerequisites are met, any hardware study is exploratory and cannot confirm or falsify P2.

*Document version 1.0*
