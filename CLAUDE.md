# CH-CHA Flux Product

PI dataset of eddy covariance ecosystem fluxes, meteorological data, and grassland management info for **CH-CHA (Chamau)**, an intensively managed grassland site in Switzerland. Part of Swiss FluxNet, Grassland Sciences Group, ETH Zurich (PI: Prof. Nina Buchmann). Produced by Lukas Hörtnagl.

**Documentation (Jupyter Book):** https://holukas.github.io/dataset_ch-cha_flux_product/intro.html  
**Dataset download:** https://www.research-collection.ethz.ch/handle/20.500.11850/747025

## Fluxes

| Variable | Description | Coverage |
|---|---|---|
| NEE | Net ecosystem exchange (CO₂) | 2005–2024 |
| LE | Latent heat flux | 2005–2024 |
| H | Sensible heat flux | 2005–2024 |
| FN2O | Nitrous oxide flux | Jan 2012 – Jul 2022 |
| FCH4 | Methane flux | Jan 2012 – Jul 2022 |

## Current Version

**CH-CHA FP2025.3** (released 16 May 2025)

## Processing Chain (Swiss FluxNet standard)

| Level | Description |
|---|---|
| L0 | Preliminary fluxes for settings refinement |
| L1 | Final EddyPro flux calculations |
| L2 | Additional quality flags |
| L3.1 | Storage-corrected fluxes (flux + storage term) |
| L3.2 | Outlier quality flags |
| L3.3 | USTAR threshold filtering — 3 scenarios: CUT_16, CUT_50, CUT_84 (for NEE, FCH4, FN2O) |
| QCF | Combined quality control flag per flux |
| L4.1 | Gap-filling (random forest primary; MDS fallback for some periods) |
| L4.2 | NEE partitioning: nighttime method (Reichstein 2005) + daytime method (Lasslop 2010) |

## Variable Naming Conventions

- Based on FLUXNET convention but with **explicit depth/height** in variable name (e.g., `SWC_GF1_0.05_1` not `SWC_1_1_1`)
- Flux versions use Level suffixes, e.g. `FN2O_L3.1_L3.3_CUT_50_QCF`
- **Timestamp:** `TIMESTAMP_MIDDLE` — middle of the 30-min averaging period (e.g., `14:15` = data from 14:00–14:30)

## Special Variable Variants

- **`MEAN3H`**: running mean over preceding 3h (calculated for SWC, TS, PREC)
- **Step-lagged**: MEAN3H lagged at 6/12/18/24 half-hour steps
- **`TIMESINCE`**: number of records since last event (for PREC and all MGMT variables, e.g., `TIMESINCE_MGMT_FERT_MIN_FOOTPRINT`)

## Repo Structure

```
docs/                          # Jupyter Book source (docs + notebooks)
  notebooks/                   # Processing notebooks, organized by step
  data/EddyPro_settings/       # EddyPro settings and metadata files
_raw/                          # Raw input data
_ETH_ResearchCollection/       # Files related to ETH Research Collection upload
myst.yml                       # JB2 config (repo root, references docs/)
pyproject.toml                 # uv project config
```

## Key External Links

- Swiss FluxNet: https://www.swissfluxnet.ethz.ch/
- Site info CH-CHA: https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-cha/
- Variable abbreviations: https://www.swissfluxnet.ethz.ch/index.php/data/variables/variable-abbreviations/
- Naming convention: https://www.swissfluxnet.ethz.ch/index.php/data/variables/naming-convention/
- GitHub issues (planned updates): https://github.com/holukas/dataset_ch-cha_flux_product/issues
