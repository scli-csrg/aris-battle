"""Export helpers for CSV and PGFPlots snippets."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List


def write_csv(path: Path, rows: Iterable[dict]) -> None:
    items = list(rows)
    if not items:
        path.write_text("", encoding="utf-8")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(items[0].keys()))
        writer.writeheader()
        writer.writerows(items)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_all_csv(out_dir: Path, results: Dict[str, List[dict]]) -> None:
    for name, rows in results.items():
        write_csv(out_dir / f"{name}.csv", rows)


def write_pgfplots(out_dir: Path, results: Dict[str, List[dict]]) -> None:
    pgf_dir = out_dir / "pgfplots"
    pgf_dir.mkdir(parents=True, exist_ok=True)
    if "jamming_sweep" in results:
        (pgf_dir / "jamming_coordinates.tex").write_text(_jamming_pgf(results["jamming_sweep"]), encoding="utf-8")
    if "sensing_trace" in results:
        (pgf_dir / "sensing_coordinates.tex").write_text(_sensing_pgf(results["sensing_trace"]), encoding="utf-8")
    if "hardware_sweep" in results:
        (pgf_dir / "hardware_matrix.tex").write_text(_hardware_pgf(results["hardware_sweep"]), encoding="utf-8")
    if "secure_communication" in results:
        (pgf_dir / "secure_ser_table.tex").write_text(_secure_ser_table(results["secure_communication"]), encoding="utf-8")


def _coordinates(rows: Iterable[dict], x_key: str, y_key: str) -> str:
    return " ".join(f"({row[x_key]},{row[y_key]})" for row in rows)


def _jamming_pgf(rows: List[dict]) -> str:
    return "\n".join(
        [
            "% Coordinates for Fig. jamming",
            "\\addplot coordinates {" + _coordinates(rows, "gain_db", "no_aris_prr") + "};",
            "\\addplot coordinates {" + _coordinates(rows, "gain_db", "attacker_aris_prr") + "};",
            "\\addplot coordinates {" + _coordinates(rows, "gain_db", "defender_aris_prr") + "};",
            "",
        ]
    )


def _sensing_pgf(rows: List[dict]) -> str:
    return "\n".join(
        [
            "% Coordinates for Fig. sensing",
            "\\addplot coordinates {" + _coordinates(rows, "time_s", "no_aris_db") + "};",
            "\\addplot coordinates {" + _coordinates(rows, "time_s", "obfuscation_db") + "};",
            "\\addplot coordinates {" + _coordinates(rows, "time_s", "counter_aris_db") + "};",
            "",
        ]
    )


def _hardware_pgf(rows: List[dict]) -> str:
    lines = ["x y C"]
    for row in rows:
        lines.append(f"{row['aris_a_elements']} {row['aris_b_elements']} {row['gain_db']}")
    return "\n".join(lines) + "\n"


def _secure_ser_table(rows: List[dict]) -> str:
    lines = ["% SER summary table", "\\begin{tabular}{llr}", "\\toprule", "Receiver & Condition & SER (\\%) \\\\", "\\midrule"]
    for row in rows:
        lines.append(f"{row['receiver']} & {row['condition']} & {row['ser_percent']} \\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    return "\n".join(lines)

