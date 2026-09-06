#!/usr/bin/env python3
"""Export reproducibility data for the acoustic ARIS battle paper."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aris_battle.experiments import model_results, paper_results, paper_summary
from aris_battle.plotting import write_all_csv, write_json, write_pgfplots


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("paper", "model"), default="paper", help="paper reproduces manuscript values; model runs deterministic sweeps")
    parser.add_argument("--out", default="results", help="output directory")
    parser.add_argument("--seed", type=int, default=2026, help="random seed for model mode")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out)
    results = paper_results() if args.mode == "paper" else model_results(seed=args.seed)
    write_all_csv(out_dir, results)
    write_pgfplots(out_dir, results)
    summary = {"mode": args.mode, "seed": args.seed if args.mode == "model" else None}
    summary.update(paper_summary() if args.mode == "paper" else {})
    write_json(out_dir / "summary.json", summary)
    print(f"Wrote {len(results)} result sets to {out_dir}")


if __name__ == "__main__":
    main()

