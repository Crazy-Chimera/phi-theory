#!/usr/bin/env python3
"""
Ω-RE Assistant – command-line entry point for Ω-Resonant Emergence.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.resonance import qualitative_resonance
from core.emergence import identify_bands, interpret_band


def load_theories(path: Path = ROOT / "registry" / "theories.yaml") -> list:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("theories", [])


def cmd_list_theories(_: argparse.Namespace) -> None:
    theories = load_theories()
    print(f"{'Name':<28} {'Status':<14} {'Ω range'}")
    print("-" * 60)
    for t in theories:
        name = t.get("name", "?")
        status = t.get("status", "?")
        dom = t.get("domain", {})
        lo = dom.get("omega_min", "?")
        hi = dom.get("omega_max", "?")
        print(f"{name:<28} {status:<14} {lo} – {hi}")


def cmd_resonance(args: argparse.Namespace) -> None:
    theories = {t["name"]: t for t in load_theories()}
    t1 = theories.get(args.t1)
    t2 = theories.get(args.t2)
    if not t1 or not t2:
        print("Unknown theory. Use 'list-theories' to see available names.")
        print("Available:", ", ".join(theories.keys()))
        sys.exit(1)

    r1 = (float(t1["domain"]["omega_min"]), float(t1["domain"]["omega_max"]))
    r2 = (float(t2["domain"]["omega_min"]), float(t2["domain"]["omega_max"]))
    R = qualitative_resonance(r1, r2)
    print(f"Qualitative R_Ω({args.t1}, {args.t2}) ≈ {R:.2f}")
    if R >= 0.8:
        print("→ Strong resonance expected (band candidate)")
    elif R >= 0.4:
        print("→ Partial resonance")
    else:
        print("→ Weak / no resonance")


def cmd_demo_bands(_: argparse.Namespace) -> None:
    omega = np.logspace(-2, 2, 2000)
    log_om = np.log10(omega)
    R = np.exp(-(log_om - 0.0) ** 2 / 0.4)
    R = np.clip(R, 0, 1)

    bands = identify_bands(omega, R, threshold=0.5)
    print(f"Found {len(bands)} resonant band(s) (threshold=0.5):\n")
    for i, b in enumerate(bands, 1):
        print(f"  Band {i}:")
        print(f"    Ω ∈ [{b['start']:.4g}, {b['end']:.4g}]")
        print(f"    center ≈ {b['center']:.4g},  max R = {b['max']:.3f}")
        print(f"    {interpret_band(b)}\n")


def cmd_run(_: argparse.Namespace) -> None:
    print("=== Ω-RE Pipeline Demo ===\n")
    theories = load_theories()
    print(f"Loaded {len(theories)} theories from registry.\n")

    print("Qualitative resonance matrix (domain overlap):\n")
    labels = [t["name"][:10] for t in theories]
    print(f"{'':14}", end="")
    for lab in labels:
        print(f"{lab:>12}", end="")
    print()

    for i, t1 in enumerate(theories):
        print(f"{labels[i]:<14}", end="")
        r1 = (float(t1["domain"]["omega_min"]), float(t1["domain"]["omega_max"]))
        for t2 in theories:
            r2 = (float(t2["domain"]["omega_min"]), float(t2["domain"]["omega_max"]))
            R = qualitative_resonance(r1, r2)
            print(f"{R:>12.2f}", end="")
        print()

    print("\n--- Demo band identification ---")
    cmd_demo_bands(_)
    print("Pipeline demo finished.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ω-RE Assistant – Ω-Resonant Emergence of Theories",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list-theories", help="List registered theories")
    p.set_defaults(func=cmd_list_theories)

    p = sub.add_parser("resonance", help="Qualitative resonance between two theories")
    p.add_argument("t1")
    p.add_argument("t2")
    p.set_defaults(func=cmd_resonance)

    p = sub.add_parser("demo-bands", help="Demonstrate band identification")
    p.set_defaults(func=cmd_demo_bands)

    p = sub.add_parser("run", help="Run full lightweight pipeline demo")
    p.set_defaults(func=cmd_run)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
