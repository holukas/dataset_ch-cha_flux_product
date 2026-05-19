"""
Merge tlag_results.csv files from all parallel parts into one file.

Reads output/04-flux_lag_pwbopt/part{n}/tlag_results.csv, concatenates them
in chronological order (sorted by period filename), and writes the merged result
to output/05-merge_results/tlag_results.csv.

Run directly in PyCharm or from the CLI:
    python 05-merge_results.py
"""

from pathlib import Path

import pandas as pd
from rich.console import Console

# ── Configuration ──────────────────────────────────────────────────────────────
# Folder containing part1/ … partN/ subfolders (produced by 04-flux_lag_pwbopt.py)
SOURCE_DIR = Path(__file__).parent.parent / 'output' / '04-flux_lag_pwbopt'

# Output folder for the merged CSV
OUT_DIR = Path(__file__).parent.parent / 'output' / '05-merge_results'

OUT_FILE = 'tlag_results.csv'
# ───────────────────────────────────────────────────────────────────────────────

console = Console()

# Locate all part result files
part_files = sorted(SOURCE_DIR.glob('part*/tlag_results.csv'))
if not part_files:
    console.print(f'[red]No tlag_results.csv files found in {SOURCE_DIR}[/]')
    raise SystemExit(1)

console.print(f'Found [bold]{len(part_files)}[/] part file(s) in [dim]{SOURCE_DIR}[/]\n')

# Read and concatenate
frames = []
for f in part_files:
    part_label = f.parent.name  # e.g. 'part1'
    df = pd.read_csv(f, na_values=['-9999', '-9999.0'])
    df.insert(0, 'part', part_label)
    frames.append(df)
    console.print(f'  [dim]{part_label}[/]  {len(df):>6} rows  →  {f}')

merged = pd.concat(frames, ignore_index=True)

# Sort chronologically by period (filename-based, lexicographic = time order)
if 'period' in merged.columns:
    merged = merged.sort_values('period').reset_index(drop=True)

# Save
OUT_DIR.mkdir(parents=True, exist_ok=True)
out_path = OUT_DIR / OUT_FILE
merged.to_csv(out_path, index=False)

# Summary
console.print(f'\n[bold green]Merged {len(merged)} rows from {len(part_files)} parts[/]')
console.print(f'Output → [bold]{out_path}[/]')

if 'period' in merged.columns:
    console.print(f'Period range: {merged["period"].iloc[0]}  →  {merged["period"].iloc[-1]}')
