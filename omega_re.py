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

from core.spectrum import build_spectrum_from_descriptor, normalize_spectrum
from core.resonance import compute_resonance, qualitative_resonance
from core.emergence import identify_bands, interpret_band, compute_kernel


def load_theories(path: Path = ROOT / "registry" / "theories.yaml") -> list:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("theories", [])


def get_theory_map() -> dict:
    return {t["name"]: t for t in load_theories()}


def build_common_grid(theories: list, n_samples: int = 5000) -> np.ndarray:
    lo = min(float(t["domain"]["omega_min"]) for t in theories)
    hi = max(float(t["domain"]["omega_max"]) for t in theories)
    lo = max(lo / 10, 1e-14)
    hi = hi * 10
    return np.logspace(np.log10(lo), np.log10(hi), n_samples)


def spectrum_of(theory: dict, omega_grid: np.ndarray) -> np.ndarray:
    spec = theory.get("spectrum")
    if spec and spec.get("peak_centers"):
        _, S = build_spectrum_from_descriptor(spec, omega_grid=omega_grid)
        return S
    lo = float(theory["domain"]["omega_min"])
    hi = float(theory["domain"]["omega_max"])
    S = np.where((omega_grid >= lo) & (omega_grid <= hi), 1.0, 0.0) + 0j
    return normalize_spectrum(S, omega_grid)


def cmd_list_theories(_: argparse.Namespace) -> None:
    theories = load_theories()
    print(f"{'Name':<28} {'Status':<14} {'Shape':<18} {'Ω range'}")
    print("-" * 78)
    for t in theories:
        name = t.get("name", "?")
        status = t.get("status", "?")
        shape = t.get("spectrum", {}).get("shape", "?")
        dom = t.get("domain", {})
        lo = dom.get("omega_min", "?")
        hi = dom.get("omega_max", "?")
        print(f"{name:<28} {status:<14} {shape:<18} {lo} – {hi}")


def cmd_resonance(args: argparse.Namespace) -> None:
    theories = get_theory_map()
    t1 = theories.get(args.t1)
    t2 = theories.get(args.t2)
    if not t1 or not t2:
        print("Unknown theory. Available:", ", ".join(theories.keys()))
        sys.exit(1)

    r1 = (float(t1["domain"]["omega_min"]), float(t1["domain"]["omega_max"]))
    r2 = (float(t2["domain"]["omega_min"]), float(t2["domain"]["omega_max"]))
    R_qual = qualitative_resonance(r1, r2)

    grid = build_common_grid([t1, t2])
    S1 = spectrum_of(t1, grid)
    S2 = spectrum_of(t2, grid)
    R_spec = compute_resonance(S1, S2, grid)

    print(f"Resonance  {args.t1}  ↔  {args.t2}")
    print(f"  qualitative (domain overlap)  R_Ω ≈ {R_qual:.3f}")
    print(f"  spectral   (peak descriptors) R_Ω ≈ {R_spec:.3f}")
    if R_spec >= 0.8:
        print("  → Strong resonance (band candidate)")
    elif R_spec >= 0.4:
        print("  → Partial resonance")
    else:
        print("  → Weak / no resonance")


def cmd_bands(args: argparse.Namespace) -> None:
    theories = get_theory_map()
    t1 = theories.get(args.t1)
    t2 = theories.get(args.t2)
    if not t1 or not t2:
        print("Unknown theory. Available:", ", ".join(theories.keys()))
        sys.exit(1)

    grid = build_common_grid([t1, t2])
    S1 = spectrum_of(t1, grid)
    S2 = spectrum_of(t2, grid)

    prod = np.abs(S1 * np.conj(S2))
    win = min(201, max(3, len(prod) // 10 * 2 + 1))
    kernel = np.ones(win) / win
    R_curve = np.convolve(prod, kernel, mode="same")
    if R_curve.max() > 0:
        R_curve = R_curve / R_curve.max()

    bands = identify_bands(grid, R_curve, threshold=args.threshold)

    print(f"Bands for  {args.t1}  ↔  {args.t2}  (threshold = {args.threshold})")
    print(f"Found {len(bands)} band(s)\n")
    for i, b in enumerate(bands, 1):
        print(f"  Band {i}:")
        print(f"    Ω ∈ [{b['start']:.4g}, {b['end']:.4g}]")
        print(f"    center ≈ {b['center']:.4g},  max R = {b['max']:.3f}")
        print(f"    {interpret_band(b)}\n")

    if args.show_kernel and bands:
        K = compute_kernel(S1, S2)
        print(f"Kernel |K| stats: min={np.abs(K).min():.3g}, max={np.abs(K).max():.3g}, median={np.median(np.abs(K)):.3g}")


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
    print("=== Ω-RE Pipeline Demo (spectral) ===\n")
    theories = load_theories()
    print(f"Loaded {len(theories)} theories from registry.\n")

    grid = build_common_grid(theories)
    spectra = {t["name"]: spectrum_of(t, grid) for t in theories}
    names = [t["name"] for t in theories]
    labels = [n[:10] for n in names]

    print("Spectral resonance matrix R_Ω:\n")
    print(f"{'':14}", end="")
    for lab in labels:
        print(f"{lab:>12}", end="")
    print()

    for i, n1 in enumerate(names):
        print(f"{labels[i]:<14}", end="")
        for n2 in names:
            R = compute_resonance(spectra[n1], spectra[n2], grid)
            print(f"{R:>12.3f}", end="")
        print()

    print("\n--- Example band: Phi-Theory ↔ QED ---")

    class Args:
        t1 = "Phi-Theory"
        t2 = "QED"
        threshold = 0.3
        show_kernel = False

    cmd_bands(Args())
    print("Pipeline demo finished.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ω-RE Assistant – Ω-Resonant Emergence of Theories",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list-theories", help="List registered theories")
    p.set_defaults(func=cmd_list_theories)

    p = sub.add_parser("resonance", help="Resonance between two theories (qualitative + spectral)")
    p.add_argument("t1")
    p.add_argument("t2")
    p.set_defaults(func=cmd_resonance)

    p = sub.add_parser("bands", help="Identify Ω-resonant bands for a pair of theories")
    p.add_argument("t1")
    p.add_argument("t2")
    p.add_argument("--threshold", type=float, default=0.3)
    p.add_argument("--show-kernel", action="store_true")
    p.set_defaults(func=cmd_bands)

    p = sub.add_parser("demo-bands", help="Synthetic band demonstration")
    p.set_defaults(func=cmd_demo_bands)

    p = sub.add_parser("run", help="Full spectral pipeline demo")
    p.set_defaults(func=cmd_run)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
