# How to contribute experimental / observational results

Software protocol (steps 1–5) is complete. **Step 6 needs real data.**

```bash
python omega_re.py predictions
python omega_re.py feedback P2 confirmed --dry-run --note "rehearsal"
python omega_re.py feedback P2 confirmed --note "DOI:… ; ΔR=…"
python tests/test_pipeline.py
```

Docs: experiment_P2_mesoscopic.md · experiment_P4_alpha.md · experimental_roadmap.md

*Contribute guide v1.0*
