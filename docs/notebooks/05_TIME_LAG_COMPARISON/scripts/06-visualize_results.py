"""
Visualize merged PWBOPT time lag results.

Loads the merged tlag_results.csv produced by 05-merge_results.py,
re-applies PWBOPT selection (standard and pre-filtered strategies), and
produces two diagnostic figures per scalar:

  1. 3-panel summary — detected lags coloured by flag, HDI range bars,
     side-by-side flag comparison between the two strategies
  2. Lag scatter + KDE — scatter of optimal lags over period index with a
     Gaussian KDE panel showing the distribution mode

Run directly in PyCharm.
"""

from pathlib import Path

import diive as dv
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ── Configuration ──────────────────────────────────────────────────────────────
# Merged CSV produced by 05-merge_results.py
RESULTS_CSV = (
        Path(__file__).parent.parent
        / 'output' / '05-merge_results' / 'tlag_results.csv'
)

# Optional: save summary PNGs here (set SAVE_PLOTS = False to skip saving)
OUT_DIR = Path(__file__).parent.parent / 'output' / '06-visualize_results'
SAVE_PLOTS = True

# Scalars present in the CSV  {display_label: column_prefix}
SCALARS = {'CH4': 'ch4', 'N2O': 'n2o'}

# PWBOPT thresholds — must match the values used in 04-flux_lag_pwbopt.py
HDI_THRESH_S = 0.5  # S1: HDI below this → reliable
DEV_THRESH_S = 0.5  # S2: max deviation from preceding optimal lag
HDI_PREFILTER_S = 2.0  # pre-filter: discard lags with HDI wider than this
LAG_MAX_S = 10.0  # used for y-axis limits on the lag panel


# ───────────────────────────────────────────────────────────────────────────────


# ── Helper functions ───────────────────────────────────────────────────────────

def apply_pwbopt(tlag_s, hdi_range_s,
                 hdi_thresh=HDI_THRESH_S, dev_thresh=DEV_THRESH_S):
    """
    Apply PWBOPT S1/S2/S3 selection logic (Vitale et al. 2024, Section 2.3).

    S1 : HDI range < hdi_thresh  → reliable, accept directly
    S2 : HDI range ≥ hdi_thresh but lag within dev_thresh of preceding optimal
         → accept for temporal continuity
    S3 : unreliable → carry forward last known optimal lag
    """
    tlag_s = np.asarray(tlag_s, dtype=float)
    hdi_range_s = np.asarray(hdi_range_s, dtype=float)
    n = len(tlag_s)
    flags = ['S3_unreliable'] * n
    optimal = np.full(n, np.nan)
    last_opt = np.nan

    for i in range(n):
        tl = tlag_s[i]
        hdi = hdi_range_s[i]

        if np.isnan(tl) or np.isnan(hdi):
            optimal[i] = last_opt
            continue

        if hdi < hdi_thresh:
            flags[i] = 'S1_optimal'
            optimal[i] = tl
            last_opt = tl
        elif not np.isnan(last_opt) and abs(tl - last_opt) <= dev_thresh:
            flags[i] = 'S2_optimal'
            optimal[i] = tl
            last_opt = tl
        else:
            optimal[i] = last_opt

    return pd.DataFrame({'pwbopt_s': optimal, 'flag': flags})


def apply_hdi_prefilter(tlag_s, hdi_range_s, threshold=HDI_PREFILTER_S):
    """Replace lags with HDI above threshold with NaN before PWBOPT runs."""
    tlag_filtered = np.asarray(tlag_s, dtype=float).copy()
    hdi = np.asarray(hdi_range_s, dtype=float)
    tlag_filtered[(hdi > threshold) & ~np.isnan(hdi)] = np.nan
    return tlag_filtered


# ── Load results ───────────────────────────────────────────────────────────────

if not RESULTS_CSV.exists():
    raise FileNotFoundError(f'Results CSV not found: {RESULTS_CSV}')

results = pd.read_csv(RESULTS_CSV, na_values=['-9999', '-9999.0'])
print(f'Loaded {len(results)} periods from {RESULTS_CSV}')

if SAVE_PLOTS:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Apply PWBOPT (standard strategy) ──────────────────────────────────────────

for scalar_label in SCALARS:
    prefix = scalar_label.lower()
    tlag_col = f'{prefix}_tlag_s'
    hdi_col = f'{prefix}_hdi_range_s'

    if tlag_col not in results.columns:
        print(f'  {scalar_label}: column {tlag_col!r} not found — skipping.')
        continue

    std = apply_pwbopt(results[tlag_col].fillna(np.nan),
                       results[hdi_col].fillna(np.nan))
    results[f'{prefix}_pwbopt_s_std'] = std['pwbopt_s']
    results[f'{prefix}_flag_std'] = std['flag']

# ── Apply pre-filtered PWBOPT ──────────────────────────────────────────────────

for scalar_label in SCALARS:
    prefix = scalar_label.lower()
    tlag_col = f'{prefix}_tlag_s'
    hdi_col = f'{prefix}_hdi_range_s'

    if tlag_col not in results.columns:
        continue

    tlag_pf = apply_hdi_prefilter(results[tlag_col].fillna(np.nan),
                                  results[hdi_col].fillna(np.nan))
    pf = apply_pwbopt(tlag_pf, results[hdi_col].fillna(np.nan))
    results[f'{prefix}_pwbopt_s_pf'] = pf['pwbopt_s']
    results[f'{prefix}_flag_pf'] = pf['flag']

# ── Summary statistics ─────────────────────────────────────────────────────────

pct_reliable = lambda col: (
    100 * np.mean(results[col].isin(['S1_optimal', 'S2_optimal']))
    if col in results.columns else np.nan
)

print('\n' + '=' * 70)
print('PWBOPT strategy comparison summary')
print('=' * 70)
print(f'\n{"Gas":<6s}  {"Strategy":<24s}  {"S1":>5s}  {"S2":>5s}  {"S3":>5s}  {"Reliable":>9s}')
print('-' * 70)

for scalar_label in SCALARS:
    prefix = scalar_label.lower()
    for strategy, flag_col in [('Standard', f'{prefix}_flag_std'),
                               ('Pre-filtered', f'{prefix}_flag_pf')]:
        if flag_col not in results.columns:
            continue
        vc = results[flag_col].value_counts()
        s1 = vc.get('S1_optimal', 0)
        s2 = vc.get('S2_optimal', 0)
        s3 = vc.get('S3_unreliable', 0)
        rel = pct_reliable(flag_col)
        print(f'  {scalar_label:<4s}  {strategy:<24s}  {s1:>5d}  {s2:>5d}  {s3:>5d}  {rel:>8.1f}%')

    hdi_col = f'{prefix}_hdi_range_s'
    if hdi_col in results.columns:
        n_pf = int(np.sum(results[hdi_col].fillna(0) > HDI_PREFILTER_S))
        print(f'         Pre-filter removed: {n_pf} / {len(results)} periods '
              f'(HDI > {HDI_PREFILTER_S} s)')
    print()

# ── Figure 1: 3-panel lag / HDI / flag summary ────────────────────────────────

FLAG_COLORS = {
    'S1_optimal': '#2ca02c',  # green  — reliable
    'S2_optimal': '#ff7f0e',  # orange — consistent
    'S3_unreliable': '#d62728',  # red    — unreliable
}

px = np.arange(len(results))  # x-axis: period index

for scalar_label in SCALARS:
    prefix = scalar_label.lower()
    tlag_col = f'{prefix}_tlag_s'
    hdi_col = f'{prefix}_hdi_range_s'
    flag_std_col = f'{prefix}_flag_std'
    flag_pf_col = f'{prefix}_flag_pf'
    opt_std_col = f'{prefix}_pwbopt_s_std'
    opt_pf_col = f'{prefix}_pwbopt_s_pf'

    if tlag_col not in results.columns:
        continue

    tlag = results[tlag_col].values.astype(float)
    hdi = results[hdi_col].values.astype(float)
    flag_std = results[flag_std_col].values
    opt_std = results[opt_std_col].values.astype(float)
    opt_pf = results[opt_pf_col].values.astype(float)

    fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
    fig.suptitle(f'{scalar_label} — PWB lag pipeline (PWBOPT strategy comparison)',
                 fontsize=12)

    # Panel 1: detected lags coloured by standard PWBOPT flag
    ax = axes[0]
    for flag, color in FLAG_COLORS.items():
        mask = flag_std == flag
        ax.scatter(px[mask], tlag[mask], color=color, s=70, zorder=3, label=flag)
    ax.plot(px, opt_std, color='black', linewidth=1.5, linestyle='-',
            label='PWBOPT standard')
    ax.plot(px, opt_pf, color='steelblue', linewidth=1.5, linestyle='--',
            label='PWBOPT pre-filtered')
    ax.set_ylabel('Time lag (s)')
    ax.set_title('Detected lags per period (coloured by standard PWBOPT flag)')
    ax.legend(frameon=False, fontsize=8, ncol=3)
    ax.set_ylim(-LAG_MAX_S - 0.5, LAG_MAX_S + 0.5)

    # Panel 2: HDI range with threshold reference lines
    ax = axes[1]
    ax.bar(px, hdi, color='#aec7e8', edgecolor='none', label='HDI range')
    ax.axhline(HDI_THRESH_S, color='#2ca02c', linewidth=1.5, linestyle='--',
               label=f'S1 threshold ({HDI_THRESH_S} s)')
    ax.axhline(HDI_PREFILTER_S, color='steelblue', linewidth=1.5, linestyle=':',
               label=f'Pre-filter threshold ({HDI_PREFILTER_S} s)')
    ax.set_ylabel('95% HDI range (s)')
    ax.set_title('Bootstrap uncertainty (HDI range) per period')
    ax.legend(frameon=False, fontsize=8)

    # Panel 3: side-by-side flag bars per period
    ax = axes[2]
    bar_w = 0.4
    for offset, flag_col in enumerate([flag_std_col, flag_pf_col]):
        for p in px:
            flag = results[flag_col].iloc[p]
            ax.bar(p + (offset - 0.5) * bar_w, 1, bar_w,
                   color=FLAG_COLORS.get(flag, '#aaaaaa'), alpha=0.85)
    patches = [mpatches.Patch(color=c, label=f) for f, c in FLAG_COLORS.items()]
    ax.legend(handles=patches, frameon=False, fontsize=8)
    ax.set_yticks([])
    ax.set_xlabel('Period index')
    ax.set_title('Flag per period: standard (left bar) vs. pre-filtered (right bar)')

    plt.tight_layout()

    if SAVE_PLOTS:
        fig.savefig(OUT_DIR / f'summary_{prefix}.png', dpi=100, bbox_inches='tight')
        print(f'Saved: {OUT_DIR / f"summary_{prefix}.png"}')

    plt.show()

# ── Figure 2: lag scatter + KDE comparison ────────────────────────────────────

scalars_plot = {}
for _label in SCALARS:
    _prefix = _label.lower()
    _col_a = f'{_prefix}_pwbopt_s_std'
    _col_b = f'{_prefix}_pwbopt_s_pf'
    if _col_a in results.columns and _col_b in results.columns:
        scalars_plot[_label] = {'col_a': _col_a, 'col_b': _col_b}

if scalars_plot:
    lag_plot = dv.PwboptLagPlot(
        results=results,
        scalars=scalars_plot,
        label_a='PWBOPT standard',
        label_b='PWBOPT pre-filtered',
        color_a='#0072B2',  # Wong blue
        color_b='#E05C2A',  # coral-orange
    )
    lag_plot.plot(
        title='PWB optimal lag: standard vs. pre-filtered PWBOPT',
        showplot=True,
        outpath=str(OUT_DIR) if SAVE_PLOTS else None,
        outname='lag_strategy_comparison.png',
    )
else:
    print('No PWBOPT columns found in results; skipping lag comparison figure.')

print('\n[OK] Visualization complete.')
if SAVE_PLOTS:
    print(f'Plots saved to: {OUT_DIR}')
