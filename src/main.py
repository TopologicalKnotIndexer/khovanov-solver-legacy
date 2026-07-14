#!/usr/bin/env python3
"""Compute integral Khovanov homology with the bundled original JavaKh."""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from de_r1 import de_r1
from input_sanity import input_sanity
from kho_solver import JavaKhError, kho_solver


UNKNOT = "q^-1*t^0*Z[0] + q^1*t^0*Z[0]"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pd_code", nargs="?", help="PD code; stdin is used when omitted")
    parser.add_argument("--java", help="Java executable, defaulting to JAVAKH_JAVA or java on PATH")
    parser.add_argument("--max-memory", default="2g", help="Java heap limit, for example 2g or 1024m")
    parser.add_argument("--timeout", type=float, default=120, help="JavaKh timeout in seconds; 0 disables it")
    args = parser.parse_args(argv)

    text = args.pd_code if args.pd_code is not None else sys.stdin.read().strip()
    try:
        pd_code = input_sanity(text)
        reduced = de_r1(pd_code)
        if not reduced:
            print(UNKNOT)
            return 0
        result = kho_solver(
            reduced,
            java_path=args.java,
            max_memory=args.max_memory,
            timeout=None if args.timeout == 0 else args.timeout,
        )
    except (ValueError, JavaKhError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
