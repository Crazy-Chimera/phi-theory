#!/usr/bin/env python3
"""Run assistant + tests and write readable reports under outputs/."""
from __future__ import annotations
import subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"

def run(name: str, cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    body = proc.stdout or ""
    if proc.stderr:
        body += "\nSTDERR:\n" + proc.stderr
    path = OUT / f"{name}.txt"
    path.write_text(body, encoding="utf-8")
    return {"name": name, "cmd": " ".join(cmd), "exit": proc.returncode, "path": str(path.relative_to(ROOT))}

def main() -> int:
    OUT.mkdir(exist_ok=True)
    py = sys.executable
    jobs = [
        ("list_theories", [py, "omega_re.py", "list-theories", "-v"]),
        ("protocol", [py, "omega_re.py", "protocol"]),
        ("predictions", [py, "omega_re.py", "predictions"]),
        ("resonance_phi_qm", [py, "omega_re.py", "resonance", "Phi-Theory", "Quantum Mechanics"]),
        ("resonance_phi_qed", [py, "omega_re.py", "resonance", "Phi-Theory", "QED"]),
        ("bands_phi_qm", [py, "omega_re.py", "bands", "Phi-Theory", "Quantum Mechanics", "--threshold", "0.25"]),
        ("run", [py, "omega_re.py", "run"]),
        ("tests", [py, "tests/test_pipeline.py"]),
        ("toy_demo", [py, "analysis/toy_mesoscopic_demo.py"]),
    ]
    results = []
    for name, cmd in jobs:
        r = run(name, cmd)
        results.append(r)
        print(f"{'OK' if r['exit']==0 else 'FAIL':8} {r['path']}")
    lines = [
        "# Omega-RE Assistant Test Report", "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}", "",
        "## Commands", "",
        "| Output file | Exit | Command |", "|-------------|------|---------|",
    ]
    for r in results:
        lines.append(f"| `{r['path']}` | {r['exit']} | `{r['cmd']}` |")
    lines += ["", "## Readable formulas", "", "$$",
              r"T(\Omega)=\int S_T(\omega)\,e^{i\omega\Omega}\,d\omega", "$$", "", "$$",
              r"R_\Omega(T_1,T_2)=\frac{\left|\int S_{T_1}S_{T_2}^*\,d\omega\right|^2}{\left(\int|S_{T_1}|^2\,d\omega\right)\left(\int|S_{T_2}|^2\,d\omega\right)}",
              "$$", "", "## Pipeline tests", "", "```",
              (OUT/"tests.txt").read_text(encoding="utf-8").strip(), "```", ""]
    (OUT/"REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote outputs/REPORT.md")
    return 1 if any(r["exit"] != 0 for r in results) else 0

if __name__ == "__main__":
    raise SystemExit(main())
