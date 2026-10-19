# Ω-RE Assistant Test Report

**Generated:** 2026-10-19 03:41 UTC

## Commands

| Output file | Exit | Command |
|-------------|------|---------|
| `outputs/list_theories.txt` | 0 | `python omega_re.py list-theories -v` |
| `outputs/protocol.txt` | 0 | `python omega_re.py protocol` |
| `outputs/predictions.txt` | 0 | `python omega_re.py predictions` |
| `outputs/resonance_phi_qm.txt` | 0 | `python omega_re.py resonance Phi-Theory "Quantum Mechanics"` |
| `outputs/resonance_phi_qed.txt` | 0 | `python omega_re.py resonance Phi-Theory QED` |
| `outputs/bands_phi_qm.txt` | 0 | `python omega_re.py bands ...` |
| `outputs/run.txt` | 0 | `python omega_re.py run` |
| `outputs/tests.txt` | 0 | `python tests/test_pipeline.py` |
| `outputs/toy_demo.txt` | 0 | `python analysis/toy_mesoscopic_demo.py` |

## Readable formulas

$$
T(\Omega)=\int S_T(\omega)\,e^{i\omega\Omega}\,d\omega
$$

$$
R_\Omega(T_1,T_2)=\frac{\left|\int S_{T_1}S_{T_2}^*\,d\omega\right|^2}{\left(\int|S_{T_1}|^2\,d\omega\right)\left(\int|S_{T_2}|^2\,d\omega\right)}
$$

## Key numeric results

| Pair | Qualitative R_Ω | Spectral R_Ω |
|------|-----------------|--------------|
| Phi-Theory ↔ Quantum Mechanics | 0.400 | **0.518** |
| Phi-Theory ↔ QED | 0.400 | **0.428** |

Pipeline tests: **All passed.**

Regenerate:

```bash
python scripts/generate_outputs.py
```
