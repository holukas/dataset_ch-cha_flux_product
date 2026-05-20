"""
Run 04-flux_lag_pwbopt.py across all input data in parallel.

Collects all .txt files from the input folder, divides them into N_PARTS equal
groups, and runs each group as an independent subprocess. Each group writes
results to output/04-flux_lag_pwbopt/part{n}/. stdout and stderr are captured
to output/04-flux_lag_pwbopt/part{n}/run.log.

Usage
-----
    python 04-run_parallel.py              # run all 8 parts
    python 04-run_parallel.py --parts 1 3 # run only parts 1 and 3
    python 04-run_parallel.py --workers 4 # limit to 4 parallel workers
"""

import argparse
import math
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, wait as futures_wait
from pathlib import Path

from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

# ── Configuration ──────────────────────────────────────────────────────────────
SCRIPT = Path(__file__).parent / '04-flux_lag_pwbopt.py'
INPUT_BASE = Path(__file__).parent.parent / 'input'
OUTPUT_BASE = Path(__file__).parent.parent / 'output' / '04-flux_lag_pwbopt'

N_PARTS = 8  # number of equal groups to split the data into
DEFAULT_WORKERS = 8  # run all parts simultaneously
MAX_FILES = None  # set to an int (e.g. 50) to cap total files processed; None = all files

INPUT_DIR = INPUT_BASE / '03-rotated_data_from_eddypro_level5'
INPUT_FILE_PATTERN = '*.txt'
# ───────────────────────────────────────────────────────────────────────────────

_part_sizes: dict[int, int] = {}  # part -> total files in that part

console = Console()


def collect_all_files() -> list[Path]:
    """Gather and sort all .txt files from the input directory."""
    if not INPUT_DIR.exists():
        raise FileNotFoundError(f'Input directory not found: {INPUT_DIR}')
    return sorted(INPUT_DIR.glob(INPUT_FILE_PATTERN))


def split_into_parts(files: list[Path], n: int) -> list[list[Path]]:
    """Divide files into n roughly equal groups."""
    chunk = math.ceil(len(files) / n)
    return [files[i:i + chunk] for i in range(0, len(files), chunk)]


def write_file_lists(groups: list[list[Path]]) -> list[Path]:
    """Write one text file per group listing the file paths; return the paths."""
    list_dir = OUTPUT_BASE / '_filelists'
    list_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, group in enumerate(groups, 1):
        p = list_dir / f'part{i}.txt'
        p.write_text('\n'.join(str(f) for f in group))
        paths.append(p)
    return paths


def count_done_per_part(parts: list[int]) -> dict[int, int]:
    """Count rows written so far per part from checkpoint CSVs."""
    done = {}
    for part in parts:
        cp = OUTPUT_BASE / f'part{part}' / 'tlag_results_checkpoint.csv'
        if cp.exists():
            try:
                with open(cp) as f:
                    done[part] = max(0, sum(1 for _ in f) - 1)
            except Exception:
                done[part] = 0
        else:
            done[part] = 0
    return done


def run_part(part: int, file_list_path: Path) -> tuple[int, int, Path]:
    output_dir = OUTPUT_BASE / f'part{part}'
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / 'run.log'

    env = {**os.environ, 'TLAG_NO_DISPLAY': '1'}

    with open(log_path, 'w') as log:
        result = subprocess.run(
            [sys.executable, str(SCRIPT),
             '--file-list', str(file_list_path),
             '--output-dir', str(output_dir)],
            stdout=log,
            stderr=log,
            env=env,
        )

    return part, result.returncode, log_path


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--parts', type=int, nargs='+',
                        help=f'which parts to run (default: all {N_PARTS})')
    parser.add_argument('--workers', type=int, default=DEFAULT_WORKERS,
                        help=f'max parallel workers (default: {DEFAULT_WORKERS})')
    args = parser.parse_args()

    # Collect and split files
    all_files = collect_all_files()
    if not all_files:
        console.print('[red]No input files found.[/]')
        sys.exit(1)
    if MAX_FILES is not None:
        all_files = all_files[:MAX_FILES]
        console.print(f'[yellow]MAX_FILES={MAX_FILES}: using first {len(all_files)} files.[/]')

    groups = split_into_parts(all_files, N_PARTS)
    file_list_paths = write_file_lists(groups)

    all_parts = list(range(1, len(groups) + 1))
    parts = args.parts if args.parts else all_parts

    for part in all_parts:
        _part_sizes[part] = len(groups[part - 1])

    files_total = len(all_files)
    console.print(f'Total files: [bold]{files_total}[/]  split into '
                  f'[bold]{len(groups)}[/] parts  '
                  f'(~{math.ceil(files_total / N_PARTS)} files each)')
    console.print(f'Running [bold]{len(parts)}[/bold] part(s) '
                  f'with [bold]{args.workers}[/bold] worker(s)')
    console.print(f'Output → {OUTPUT_BASE}\n')

    failed = []

    with Progress(
            TextColumn('  {task.description}'),
            BarColumn(bar_width=28),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console,
            refresh_per_second=4,
    ) as progress:

        # One progress task per part + one overall task
        task_ids: dict[int, int] = {}
        for part in all_parts:
            task_ids[part] = progress.add_task(
                f'[dim]part{part}  ○[/]',
                total=_part_sizes[part],
                visible=True,
            )
        overall = progress.add_task('[bold]Total[/]', total=files_total)

        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_map = {
                executor.submit(run_part, part, file_list_paths[part - 1]): part
                for part in parts
            }

            # Mark submitted parts as running
            for part in parts:
                progress.update(task_ids[part], description=f'[yellow]part{part}  ●[/]')

            pending = set(future_map)
            while pending:
                # Wait up to 0.5 s or until the next future completes
                done_futures, pending = futures_wait(pending, timeout=0.5)

                for f in done_futures:
                    part, returncode, log_path = f.result()
                    if returncode != 0:
                        failed.append(part)
                        progress.update(task_ids[part],
                                        description=f'[red]part{part}  ✗[/]',
                                        completed=_part_sizes[part])
                    else:
                        progress.update(task_ids[part],
                                        description=f'[green]part{part}  ✓[/]',
                                        completed=_part_sizes[part])

                # Refresh per-part counts from checkpoint files for still-running parts
                still_running = [future_map[f] for f in pending]
                done_counts = count_done_per_part(still_running)
                for part, done_count in done_counts.items():
                    progress.update(task_ids[part], completed=done_count)

                # Update overall bar
                total_done = sum(count_done_per_part(all_parts).values())
                progress.update(overall, completed=total_done)

    console.print()
    if failed:
        for part in failed:
            log = OUTPUT_BASE / f'part{part}' / 'run.log'
            console.print(f'  [bold red]✗ part{part} failed[/] → check {log}')
        sys.exit(1)

    console.print('[bold green]All parts completed successfully.[/]')


if __name__ == '__main__':
    main()
