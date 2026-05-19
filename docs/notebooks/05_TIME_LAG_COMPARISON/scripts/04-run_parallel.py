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
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.text import Text

# ── Configuration ──────────────────────────────────────────────────────────────
SCRIPT = Path(__file__).parent / '04-flux_lag_pwbopt.py'
INPUT_BASE = Path(__file__).parent.parent / 'input'
OUTPUT_BASE = Path(__file__).parent.parent / 'output' / '04-flux_lag_pwbopt'

N_PARTS = 8  # number of equal groups to split the data into
DEFAULT_WORKERS = 8  # run all parts simultaneously

INPUT_DIR = INPUT_BASE / '03-rotated_data_from_eddypro_level5'
INPUT_FILE_PATTERN = '*.txt'
# ───────────────────────────────────────────────────────────────────────────────

# Shared state updated by worker threads
_states: dict[int, str] = {}  # part -> 'pending' | 'running' | 'ok' | 'failed'
_part_sizes: dict[int, int] = {}  # part -> total files in that part
_lock = threading.Lock()

BAR_WIDTH = 24

SYMBOLS = {
    'pending': ('○', 'dim white'),
    'running': ('●', 'yellow'),
    'ok': ('✓', 'bold green'),
    'failed': ('✗', 'bold red'),
}

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


def _format_eta(seconds: float) -> str:
    if seconds < 0:
        return '—'
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f'{h}h {m:02d}m {s:02d}s'
    if m > 0:
        return f'{m}m {s:02d}s'
    return f'{s}s'


def make_display(parts: list[int], done_per_part: dict[int, int],
                 files_total: int, start_time: float) -> Text:
    text = Text()

    # One line per part: symbol + bar + count
    for part in parts:
        state = _states.get(part, 'pending')
        sym, sym_style = SYMBOLS[state]
        total_part = _part_sizes.get(part, 0)
        done_part = done_per_part.get(part, 0)
        pct_part = done_part / total_part if total_part > 0 else 0.0
        filled = int(pct_part * BAR_WIDTH)

        text.append(f'  part{part} ')
        text.append(sym, style=sym_style)
        text.append('  ')
        text.append('█' * filled, style='bold green')
        text.append('░' * (BAR_WIDTH - filled), style='dim')
        text.append(f'  {done_part:>{len(str(total_part))}} / {total_part}')
        text.append(f'  ({pct_part * 100:5.1f}%)\n', style='cyan')

    # Overall progress + ETA
    files_done = sum(done_per_part.values())
    pct = files_done / files_total * 100 if files_total > 0 else 0.0
    elapsed = time.monotonic() - start_time
    rate = files_done / elapsed if elapsed > 0 and files_done > 0 else 0.0
    remaining = (files_total - files_done) / rate if rate > 0 else -1

    text.append(f'\n  Total: ')
    text.append(f'{files_done} / {files_total}', style='bold')
    text.append(f'  ({pct:.1f}%)', style='cyan')
    text.append(f'  ETA: ')
    text.append(_format_eta(remaining), style='magenta')

    return text


def _monitor(parts: list[int], total: int, start_time: float,
             live: Live, stop: threading.Event) -> None:
    """Background thread: refresh the display every 0.5s with latest file counts."""
    while not stop.is_set():
        done_per_part = count_done_per_part(parts)
        live.update(make_display(parts, done_per_part, total, start_time))
        stop.wait(0.5)


def run_part(part: int, file_list_path: Path) -> tuple[int, int, Path]:
    output_dir = OUTPUT_BASE / f'part{part}'
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / 'run.log'

    with _lock:
        _states[part] = 'running'

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

    with _lock:
        _states[part] = 'ok' if result.returncode == 0 else 'failed'

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

    groups = split_into_parts(all_files, N_PARTS)
    file_list_paths = write_file_lists(groups)

    all_parts = list(range(1, len(groups) + 1))
    parts = args.parts if args.parts else all_parts

    for part in all_parts:
        _states[part] = 'pending'
        _part_sizes[part] = len(groups[part - 1])

    files_total = len(all_files)
    console.print(f'Total files: [bold]{files_total}[/]  split into '
                  f'[bold]{len(groups)}[/] parts  '
                  f'(~{math.ceil(files_total / N_PARTS)} files each)')
    console.print(f'Running [bold]{len(parts)}[/bold] part(s) '
                  f'with [bold]{args.workers}[/bold] worker(s)')
    console.print(f'Output → {OUTPUT_BASE}\n')

    failed = []
    stop_event = threading.Event()
    start_time = time.monotonic()

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(run_part, part, file_list_paths[part - 1]): part
            for part in parts
        }

        with Live(make_display(parts, {}, files_total, start_time), console=console,
                  refresh_per_second=4, transient=False) as live:

            monitor = threading.Thread(
                target=_monitor, args=(parts, files_total, start_time, live, stop_event),
                daemon=True,
            )
            monitor.start()

            for f in as_completed(futures):
                part, returncode, log_path = f.result()
                if returncode != 0:
                    failed.append(part)

            stop_event.set()

    console.print()
    if failed:
        for part in failed:
            log = OUTPUT_BASE / f'part{part}' / 'run.log'
            console.print(f'  [bold red]✗ part{part} failed[/] → check {log}')
        sys.exit(1)

    console.print('[bold green]All parts completed successfully.[/]')


if __name__ == '__main__':
    main()
