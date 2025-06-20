#!/usr/bin/env python3
"""Template script to generate strained QE inputs and post-process λ.

Not fully automated yet – serves as scaffolding for SIM-1 task.
"""
import argparse
import pathlib
import subprocess
from typing import List

TEMPLATE = pathlib.Path(__file__).resolve().parent.parent / "reference" / "scf.in"

HEADER = "Generated by run_strain_scan.py – edit as needed\n"

def write_inputs(a0: float, b0: float, c: float, eps_list: List[int]):
    for eps in eps_list:
        strain = eps / 100.0
        a = a0 * (1 + strain)
        b = b0 * (1 + strain)
        folder = pathlib.Path(f"strain_{eps:+d}pc")
        folder.mkdir(exist_ok=True)
        text = TEMPLATE.read_text()
        text = text.replace("3.520", f"{a:.6f}", 1)
        text = text.replace("-1.760  3.050", f"{-a/2:.3f}  {b*0.8660:.3f}", 1)
        (folder / "scf.in").write_text(HEADER + text)
        # minimal ph input
        (folder / "ph.in").write_text("&INPUTPH\n  prefix='Li2NH_ci'\n/\n")
        print(f"✓ wrote {folder}/scf.in")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--a0", type=float, required=True)
    p.add_argument("--b0", type=float, required=True)
    p.add_argument("--c", type=float, required=True)
    p.add_argument("--eps", nargs="+", type=int, required=True,
                   help="strain percentages e.g. -3 -2 -1 0 1 2 3")
    p.add_argument("--post", action="store_true", help="only post-process λ")
    args = p.parse_args()

    if args.post:
        print("Post-processing not yet implemented – SIM-1 task.")
    else:
        write_inputs(args.a0, args.b0, args.c, args.eps)

if __name__ == "__main__":
    main() 