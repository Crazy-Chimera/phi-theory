# Ω-RE / Phi-Theory repository status

**Updated:** 2026-10-19  
**Registry:** theories v1.3.1 · predictions v1.1.0 · resonances v1.1.0

## Protocol progress (6 steps)

| Step | Status |
|------|--------|
| 1 Spectral decomposition | done |
| 2 Resonance matrix | done |
| 3 Band identification | done |
| 4 Emergent kernel | done |
| 5 Prediction generation | done (P1–P6) |
| 6 Feedback | in progress (P2 undecided) |

Details: `docs/protocol_log.md`

## Predictions

| ID | Pair | R_Ω | Status | Doc |
|----|------|-----|--------|-----|
| P1 | Phi ↔ LQG | 0.591 | untested | — |
| P2 | Phi ↔ QM | 0.518 | **undecided** | `docs/experiment_P2_mesoscopic.md` |
| P3 | Phi ↔ SM | 0.453 | untested | — |
| P4 | Phi ↔ QED | 0.428 | untested | `docs/experiment_P4_alpha.md` |
| P5 | Phi ↔ GR | 0.225 | untested | — |
| P6 | Classical ↔ QM | ~0 | untested | — |

## Assistant

```bash
python omega_re.py list-theories -v
python omega_re.py run
python omega_re.py predictions
python omega_re.py feedback <id> confirmed|falsified|undecided [--note "..."]
python omega_re.py bands "Phi-Theory" "Quantum Mechanics" --show-kernel
```
