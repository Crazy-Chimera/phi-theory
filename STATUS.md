# Ω-RE / Phi-Theory repository status

**Updated:** 2026-10-19  
**Registry:** theories v1.3.1 · predictions v1.1.0

## Theories (7)

Each entry includes: equations, domain, spectrum descriptors, **verification**, **relevance_to_phi**.

| Theory | Status | Spectral role |
|--------|--------|----------------|
| Phi-Theory | speculative | Core; master equation |
| QED | confirmed | Precision α / g-2 |
| General Relativity | confirmed | G(Φ) limit |
| Classical Mechanics | confirmed (regime-limited) | Mesoscopic boundary |
| Quantum Mechanics | confirmed | Entanglement / observer |
| Quantum Gravity (LQG) | speculative | Discrete geometry |
| Standard Model | confirmed (gaps) | Topological defects |

## Predictions protocol

| ID | Pair | R_Ω | Status | Observable |
|----|------|------|--------|------------|
| P1 | Phi ↔ LQG | 0.591 | untested | ΔA/A_Planck |
| P2 | Phi ↔ QM | 0.518 | **undecided** | ΔR mesoscopic |
| P3 | Phi ↔ SM | 0.453 | untested | Δy_f/y_f |
| P4 | Phi ↔ QED | 0.428 | untested | Δα/α |
| P5 | Phi ↔ GR | 0.225 | untested | ΔG/G |
| P6 | Classical ↔ QM | ~0 | untested | ΔS_classical |

P2 experiment design: `docs/experiment_P2_mesoscopic.md`

## Assistant commands

```bash
python omega_re.py list-theories -v   # verification + relevance
python omega_re.py resonance T1 T2
python omega_re.py bands T1 T2 [--threshold 0.3]
python omega_re.py run               # matrix + predictions protocol
python omega_re.py predictions
python omega_re.py feedback <id> confirmed|falsified|undecided|untested [--note "..."]
```

## Feedback loop

- confirmed → strengthen band
- falsified → weaken band
- log: `registry/resonances.yaml`
