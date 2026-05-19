# Time Lag Comparison

Test comparison of different EddyPro time lag detection settings using 2021 data, run for both LGR and QCL instruments. Results inform the final time lag settings used in the main flux processing chain.

## Folder Structure

```
05_TIME_LAG_COMPARISON/
  scripts/
    04-flux_lag_pwbopt.py     PWB time lag detection (single run or called by parallel runner)
    04-run_parallel.py        Parallel runner: splits input into 8 groups, runs simultaneously
    05-merge_results.py       Merge per-part tlag_results.csv files into one (run in PyCharm)
    06-visualize_results.py   Visualize merged results: PWBOPT plots + KDE (run in PyCharm)
  eddypro_settings/           EddyPro settings for each of the 10 test variants
  input/                      High-frequency input files (gitignored)
    03-rotated_data_from_eddypro_level5/   All EddyPro-rotated .txt files (one per 30-min period)
  output/                     Results (gitignored)
    04-flux_lag_pwbopt/       Produced by 04-flux_lag_pwbopt.py
      part1/ … part8/         One subfolder per parallel group, each with:
        tlag_results.csv              detected lags and PWBOPT flags
        tlag_results_checkpoint.csv   checkpoint for crash recovery
        plots/                        diagnostic PNGs per period and summary figures
        run.log                       stdout/stderr from the subprocess
      _filelists/             Auto-generated file lists for splitting input across 8 workers
    05-merge_results/         Produced by 05-merge_results.py
      tlag_results.csv        All parts merged and sorted chronologically
    06-visualize_results/     Produced by 06-visualize_results.py
      summary_ch4.png         3-panel summary figure for CH4
      summary_n2o.png         3-panel summary figure for N2O
      lag_strategy_comparison.png   Scatter + KDE comparison of PWBOPT strategies
```

## Variants

10 variants in total: 5 settings × 2 instruments (LGR, QCL). See [`eddypro_settings/README.md`](eddypro_settings/README.md) for details.

## Scripts

### `04-flux_lag_pwbopt.py`

Batch PWB (pre-whitening with block-bootstrap) time lag detection across all 30-min periods,
followed by PWBOPT optimal lag selection (Vitale et al., 2024).

**What it does:**

1. Loads EddyPro-rotated high-frequency files from `input/`
2. Runs PWB detection for each period and scalar (CH4, N2O)
3. Applies PWBOPT S1/S2/S3 selection logic to pick the optimal lag per period:
   - **S1**: HDI range < 0.5 s → reliable, accept directly
   - **S2**: HDI range ≥ 0.5 s but lag is within 0.5 s of the preceding optimal → accept for temporal continuity
   - **S3**: unreliable → carry forward last known optimal lag
4. Compares two PWBOPT strategies:
   - **Standard**: apply S1/S2/S3 directly on all detected lags
   - **Pre-filtered**: first discard lags with HDI > 1.0 s, then apply S1/S2/S3
5. Saves results to `output/04-flux_lag_pwbopt/` and diagnostic plots to `output/04-flux_lag_pwbopt/plots/`

**Key settings** (top of script):

| Setting | Default | Description |
|---|---|---|
| `USE_SYNTHETIC` | `False` | `True` runs a self-contained demo on synthetic data |
| `INPUT_DIR` | see script | Folder with EddyPro-rotated high-frequency files |
| `OUTPUT_DIR` | `output/04-flux_lag_pwbopt/` | Results and plots destination |
| `LAG_MAX_S` | 10.0 s | CCF search half-width |
| `HDI_THRESH_S` | 0.5 s | S1 reliability threshold |
| `HDI_PREFILTER_S` | 1.0 s | Pre-filter threshold for wide-HDI lags |
| `RESULTS_CSV` | `None` | Set to a previous CSV to skip detection and re-run PWBOPT only |

### `04-run_parallel.py`

Parallel runner for `04-flux_lag_pwbopt.py`. Collects all `.txt` files from the input folder,
splits them into 8 equal groups, and runs each group as an independent subprocess with a
live progress display (per-part progress bars + overall ETA).

**Key settings** (top of script):

| Setting | Default | Description |
|---|---|---|
| `N_PARTS` | 8 | Number of equal file groups |
| `DEFAULT_WORKERS` | 8 | Max parallel subprocesses |

### `05-merge_results.py`

Merges the `tlag_results.csv` files from all parallel parts into a single chronologically
sorted file. Reads from `output/04-flux_lag_pwbopt/part*/tlag_results.csv` and writes to
`output/05-merge_results/tlag_results.csv`. Run directly in PyCharm (no CLI args needed).

### `06-visualize_results.py`

Loads the merged `tlag_results.csv`, re-applies PWBOPT selection (standard and pre-filtered
strategies), and produces two figures per scalar:

1. **3-panel summary** — detected lags coloured by S1/S2/S3 flag, 95% HDI range bars with
   threshold lines, side-by-side flag comparison between strategies
2. **Scatter + KDE** — optimal lag scatter over period index with a Gaussian KDE panel
   showing the distribution mode (`dv.PwboptLagPlot`)

Run directly in PyCharm. Figures are saved to `output/06-visualize_results/`.

**Key settings** (top of script):

| Setting | Default | Description |
|---|---|---|
| `RESULTS_CSV` | `output/05-merge_results/tlag_results.csv` | Merged CSV to visualize |
| `OUT_DIR` | `output/06-visualize_results/` | Folder for saved PNGs |
| `SAVE_PLOTS` | `True` | Save figures as PNG |
| `HDI_THRESH_S` | 0.5 s | S1 threshold (must match 04) |
| `HDI_PREFILTER_S` | 1.0 s | Pre-filter threshold (must match 04) |

## How to Run

From the repo root:

```bash
# run all 8 parts in parallel (recommended)
uv run python docs/notebooks/05_TIME_LAG_COMPARISON/scripts/04-run_parallel.py

# run only specific parts
uv run python docs/notebooks/05_TIME_LAG_COMPARISON/scripts/04-run_parallel.py --parts 1 2 3

# limit parallel workers (e.g. if RAM is tight)
uv run python docs/notebooks/05_TIME_LAG_COMPARISON/scripts/04-run_parallel.py --workers 4
```

Or from the `scripts/` folder:

```bash
uv run python 04-run_parallel.py
```

## Analysis Ideas

### 1. Time lag distributions
- Plot histograms of detected time lags per variant
- Check whether detected lags are stable and physically plausible
- Compare LGR vs. QCL distributions for the same settings

### 2. Data coverage
- Calculate the fraction of records flagged S1, S2, S3 per variant
- A variant with mostly S3 flags is unreliable regardless of flux values

### 3. Time series overlay
- Plot flux values (FN2O, FCH4) from all variants over a representative period
- Reveals systematic offsets or divergence between variants

### 4. Scatter plots vs. reference
- Use one variant as reference (e.g. 0–10s with default)
- Plot all other variants against it
- Quantify bias and scatter (RMSE, slope, R²)

### 5. Summary statistics
- Mean, median, and RMSE of fluxes per variant relative to reference
- Summarize S1/S2/S3 fractions per variant

## Suggested Workflow

1. Start with **time lag distributions** and **S1/S2/S3 fractions** to eliminate poorly performing variants
2. Use **scatter plots** and **summary statistics** to compare the remaining candidates
3. Use **time series overlays** to check for seasonal or event-driven differences

## Reference

Vitale, D., et al. (2024). A pre-whitening with block-bootstrap cross-correlation procedure
for temporal alignment of eddy covariance data. *Environmental and Ecological Statistics*,
31, 219–244. https://doi.org/10.1007/s10651-024-00615-9
