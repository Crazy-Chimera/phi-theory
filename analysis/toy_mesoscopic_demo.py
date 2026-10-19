"""Toy demo: synthetic mesoscopic residual vs Omega-proxy (illustrative only)."""
from __future__ import annotations
import numpy as np

def simulate_residual(
    n_points: int = 40,
    true_delta: float = 0.03,
    noise: float = 0.008,
    band_center: float = 0.0027,
    band_width: float = 1.5,
    seed: int = 42,
) -> dict:
    rng = np.random.default_rng(seed)
    omega = np.logspace(-5, -1, n_points)
    log_om = np.log10(omega)
    log_c = np.log10(band_center)
    signal = true_delta * np.exp(-0.5 * ((log_om - log_c) / band_width) ** 2)
    residual = signal + rng.normal(0, noise, size=n_points)
    in_band = (omega >= 3.39e-5) & (omega <= 0.216)
    mean_in = float(np.mean(residual[in_band]))
    mean_out = float(np.mean(residual[~in_band])) if np.any(~in_band) else 0.0
    detected = abs(mean_in) > 2 * noise and abs(mean_in) > abs(mean_out)
    return {
        "mean_in_band": mean_in,
        "mean_out_band": mean_out,
        "noise": noise,
        "detected": detected,
        "suggested_feedback": "confirmed" if detected else "falsified",
    }

def main() -> None:
    r = simulate_residual()
    print("=== Toy mesoscopic residual demo (NOT real data) ===")
    print(f"mean dR in P2 band:  {r['mean_in_band']:+.4f}")
    print(f"mean dR outside:     {r['mean_out_band']:+.4f}")
    print(f"noise sigma:         {r['noise']:.4f}")
    print(f"detection heuristic: {r['detected']}")
    print(f"suggested feedback:  {r['suggested_feedback']}")
    print()
    print("If this were real data:")
    print(f"  python omega_re.py feedback P2 {r['suggested_feedback']} --note \"toy demo only\"")

if __name__ == "__main__":
    main()
