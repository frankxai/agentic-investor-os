#!/usr/bin/env python3
"""Educational two-stage DCF. Illustrative simulation only. Not a verdict."""
from __future__ import annotations

import argparse
import sys


def pv(cashflow: float, wacc: float, t: int) -> float:
    if wacc <= -1:
        raise ValueError("wacc must be greater than -100%")
    return cashflow / ((1.0 + wacc) ** t)


def two_stage_dcf(
    fcf0: float,
    g1: float,
    years1: int,
    g_terminal: float,
    wacc: float,
) -> dict[str, float]:
    """Toy two-stage model. Fails closed if WACC <= terminal growth."""
    if years1 < 1:
        raise ValueError("years1 must be >= 1")
    if wacc <= g_terminal:
        raise ValueError("this toy model requires wacc > terminal growth")
    stage1 = 0.0
    fcf = fcf0
    for t in range(1, years1 + 1):
        fcf = fcf * (1.0 + g1)
        stage1 += pv(fcf, wacc, t)
    terminal_fcf = fcf * (1.0 + g_terminal)
    terminal_value = terminal_fcf / (wacc - g_terminal)
    stage2 = pv(terminal_value, wacc, years1)
    return {
        "stage1_pv": stage1,
        "terminal_pv": stage2,
        "enterprise_value_toy": stage1 + stage2,
    }


def self_test() -> int:
    out = two_stage_dcf(fcf0=100.0, g1=0.05, years1=5, g_terminal=0.02, wacc=0.10)
    if out["enterprise_value_toy"] <= 0:
        print("self-test failed: non-positive value", file=sys.stderr)
        return 1
    try:
        two_stage_dcf(100.0, 0.05, 5, 0.10, 0.08)
    except ValueError:
        pass
    else:
        print("self-test failed: expected fail-closed WACC gate", file=sys.stderr)
        return 1
    print("dcf educational self-test passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Educational DCF simulation")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
