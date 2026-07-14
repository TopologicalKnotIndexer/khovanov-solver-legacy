"""Parse and structurally validate a planar diagram code."""

from __future__ import annotations

import ast
from collections import Counter


def input_sanity(input_string: str) -> list[list[int]]:
    try:
        value = ast.literal_eval(input_string)
    except (SyntaxError, ValueError) as exc:
        raise ValueError("PD code must be a Python/JSON-style nested list") from exc
    if not isinstance(value, list):
        raise ValueError("PD code must be a list")

    pd_code: list[list[int]] = []
    counts: Counter[int] = Counter()
    for crossing in value:
        if not isinstance(crossing, (list, tuple)) or len(crossing) != 4:
            raise ValueError("every PD crossing must contain exactly four entries")
        normalized: list[int] = []
        for label in crossing:
            if isinstance(label, bool) or not isinstance(label, int) or label <= 0:
                raise ValueError("PD labels must be positive integers")
            normalized.append(label)
            counts[label] += 1
        pd_code.append(normalized)

    bad = {label: count for label, count in counts.items() if count != 2}
    if bad:
        raise ValueError(f"every PD label must occur exactly twice: {bad}")
    return pd_code


if __name__ == "__main__":
    print(input_sanity("[[1,2,2,1]]"))
