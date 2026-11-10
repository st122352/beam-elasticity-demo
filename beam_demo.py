"""Analytical Euler-Bernoulli solution for a cantilever with a tip force.

Sign convention: positive force and deflection are downward. All input values
use SI units: metres, newtons, pascals, and metres to the fourth for I.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Beam:
    length_m: float
    force_n: float
    young_pa: float
    inertia_m4: float

    def __post_init__(self) -> None:
        for name in ("length_m", "force_n", "young_pa", "inertia_m4"):
            value = getattr(self, name)
            if value <= 0:
                raise ValueError(f"{name} must be positive")

    def response(self, x_m: float) -> tuple[float, float, float]:
        """Return downward deflection [m], slope [rad], and |moment| [N m]."""
        if not 0.0 <= x_m <= self.length_m:
            raise ValueError("x_m must lie between 0 and length_m")
        p, x, length = self.force_n, x_m, self.length_m
        ei = self.young_pa * self.inertia_m4
        deflection = p * x**2 * (3.0 * length - x) / (6.0 * ei)
        slope = p * x * (2.0 * length - x) / (2.0 * ei)
        moment = p * (length - x)
        return deflection, slope, moment


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--length", type=float, default=1.0, help="beam length [m]")
    parser.add_argument("--force", type=float, default=100.0, help="downward tip force [N]")
    parser.add_argument("--young", type=float, default=200e9, help="Young's modulus [Pa]")
    parser.add_argument("--inertia", type=float, default=1e-6, help="second moment of area [m^4]")
    parser.add_argument("--points", type=int, default=5, help="number of output points, including ends")
    args = parser.parse_args()
    if args.points < 2:
        parser.error("--points must be at least 2")

    beam = Beam(args.length, args.force, args.young, args.inertia)
    print("x_m,deflection_down_m,slope_rad,moment_magnitude_Nm")
    for i in range(args.points):
        x = beam.length_m * i / (args.points - 1)
        v, theta, moment = beam.response(x)
        print(f"{x:.6g},{v:.9g},{theta:.9g},{moment:.9g}")


if __name__ == "__main__":
    main()

