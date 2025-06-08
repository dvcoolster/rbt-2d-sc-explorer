#!/usr/bin/env python3
"""
check_phonon_stability.py
=========================

Quick sanity checker for Quantum-Espresso phonon calculations.
Given one or more `*.dyn[mat]` or `*.freq` files produced by `ph.x`, the tool
parses the phonon frequencies and flags imaginary (negative) modes.  It prints
an overall ✅ / ⚠️ summary that can be consumed by CI pipelines.

Usage
-----
$ python scripts/check_phonon_stability.py pwscf.dyn{0..8}
$ check_phonon_stability pwscf.freq

Exit codes
----------
0 – all modes stable (no imaginary frequencies)
1 – imaginary modes found (unstable)
2 – error parsing files
"""
from __future__ import annotations
import sys
import re
import pathlib
from typing import List, Tuple

FREQ_REGEX = re.compile(r"freq\(.*?\)=\s*([\-0-9\.]+)")


def parse_frequencies(path: pathlib.Path) -> List[float]:
    """Return list of frequencies (cm^-1) found in a QE .dyn/.freq file."""
    freqs: List[float] = []
    try:
        with path.open("r", errors="ignore") as fh:
            for line in fh:
                m = FREQ_REGEX.search(line)
                if m:
                    freqs.append(float(m.group(1)))
    except Exception as exc:
        raise RuntimeError(f"Cannot read {path}: {exc}")
    if not freqs:
        raise RuntimeError(f"No frequencies found in {path}")
    return freqs


def analyse_files(files: List[pathlib.Path]) -> Tuple[int, int, float]:
    """Return (n_total, n_imag, min_freq)."""
    total = 0
    imag = 0
    min_freq = 1e9
    for f in files:
        freqs = parse_frequencies(f)
        total += len(freqs)
        imag += sum(1 for w in freqs if w < 0)
        min_freq = min(min_freq, min(freqs))
    return total, imag, min_freq


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    paths = [pathlib.Path(p) for p in sys.argv[1:]]
    for p in paths:
        if not p.exists():
            print(f"ERROR: {p} does not exist", file=sys.stderr)
            sys.exit(2)

    try:
        total, imag, min_freq = analyse_files(paths)
    except RuntimeError as err:
        print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(2)

    if imag == 0:
        print(f"✅ Stable phonon spectrum – {total} modes, min ω = {min_freq:.2f} cm^-1")
        sys.exit(0)
    else:
        pct = imag / total * 100
        print(f"⚠️  {imag}/{total} modes imaginary ({pct:.1f}%), min ω = {min_freq:.2f} cm^-1")
        sys.exit(1)


if __name__ == "__main__":
    main() 