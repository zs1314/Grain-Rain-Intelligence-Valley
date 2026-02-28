"""Command line interface for rainfall analysis."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from .analytics import analyze_rainfall, suggest_action


def _read_csv(path: Path) -> list[float]:
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if "rainfall_mm" not in (reader.fieldnames or []):
            raise ValueError("CSV must include 'rainfall_mm' column")

        samples: list[float] = []
        for row in reader:
            raw = (row.get("rainfall_mm") or "").strip()
            if not raw:
                continue
            samples.append(float(raw))

    return samples


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: griv-analyze <path-to-rainfall-csv>")

    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        raise SystemExit(f"File not found: {csv_path}")

    report = analyze_rainfall(_read_csv(csv_path))
    payload = report.to_dict()
    payload["recommendation"] = suggest_action(report)

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
