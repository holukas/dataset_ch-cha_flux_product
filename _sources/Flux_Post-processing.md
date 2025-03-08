# Flux Post-processing

- Post-processing follows the [Swiss Fluxnet Flux Processing Chain](https://www.swissfluxnet.ethz.ch/index.php/data/ecosystem-fluxes/flux-processing-chain/)
## Overview

```{mermaid}

    flowchart
        L1F[L1 fluxes]
        L2QCF[L2 quality flags]
        L31F[L3.1 fluxes]
        L31Ffiltered[L3.1 fluxes filtered]
        L32QCF[L3.2 quality flags]
        L33QCF[L3.3 quality flags]
        QCF[overall quality flag QCF]
        L31FfilteredQCF[L3.1 fluxes filtered with QCF]
        L41F[L4.1 gap-filled fluxes]
        L42F[L4.2 partitioned fluxes]
        
        L1F --> L2QCF
        L2QCF --> L31Ffiltered
        L1F --> L31F
        L31F --> L31Ffiltered
        L31Ffiltered --> L32QCF
        L1F --> L33QCF
        
        L2QCF --> QCF
        L32QCF --> QCF
        L33QCF --> QCF
        
        QCF -- applied to storage-corrected fluxes --> L31FfilteredQCF
        L31FfilteredQCF -- gap-filling --> L41F
        
        L41F -- partitioning (NEE) --> L42F

```

- **Level-2** creates additional quality flags that are then combined to one overall quality flag `QCF` (quality control flag)
- **Level-3.1** adds the storage term to the respective flux
- **Level-3.2** detects outliers and creates additional quality flags
- **Level-3.3** creates additional quality flags based on three different constant USTAR thresholds, previously detected by FLUXNET (Pastorello et al., 2020)
- **Level-4.1** performs gap-filling (long-term random forest)
- (planned) **Level-4.2** partitions NEE fluxes into GPP and RECO

## QCF: overall quality control flag after Level-3.3 tests
*See below for a description of how `QCF` is calculated.*
- **For subsequent steps (Level-4.1+), fully quality-filtered fluxes are needed.**
- Therefore, after running the individual quality tests in previous steps, the single flags are combined into the overall `QCF`.
- This creates flux variables that have been filtered by all quality flags created in Level-2, Level-3.2 and Level-3.3.
- The overall quality flag after Level-3.3 is named `FLAG_L3.3_<ustar_scenario>_<flux>_QCF`.
- **Example** for NEE: 
	- `FLAG_L3.3_CUT_50_NEE_L3.1_QCF` is the `QCF` for `NEE_L3.1` after Level-3.3.
	- This flag is used to filter the variable `NEE_L3.1` and creates the quality-filtered variable `NEE_L3.1_L3.3_CUT_50_QCF`, that is then used in the following steps.
	- Note that `NEE_L3.1` is the unfiltered, but storage-corrected variable `FC` from the flux calculations.
- **Examples** for `<ustar_scenario>`:
	- `CUT_16`, `CUT_50`, `CUT_84`
- **Examples** for `<flux>`:
	- `FC_L3.1`, `LE_L3.1`, `H_L3.1`, `FN2O_L3.1`, `FCH4_L3.1`
	- These are fluxes that are storage-corrected (Level-3.1), but are not filtered yet.
- **Example** output from diive for `NEE_L3.1` (storage-corrected `FC` from Level-3.1) for the USTAR scenario `CUT_50`, detailing the sequential application of all individual quality flags from Level-2, Level-3.2 and Level-3.3: 
```
========================================
QCF FLAG EVOLUTION
========================================
This output shows the evolution of the QCF overall quality flag
when test flags are applied sequentially to the variable NEE_L3.1.

Number of NEE_L3.1 records before QC: 295350
+++ FLAG_L2_FC_MISSING_TEST rejected 0 values (+0.00%)      TOTALS: flag 0: 295350 (100.00%) / flag 1: 0 (0.00%) / flag 2: 0 (0.00%)
+++ FLAG_L2_FC_SSITC_TEST rejected 133899 values (+45.34%)      TOTALS: flag 0: 115080 (38.96%) / flag 1: 46371 (15.70%) / flag 2: 133899 (45.34%)
+++ FLAG_L2_FC_COMPLETENESS_TEST rejected 690 values (+0.23%)      TOTALS: flag 0: 114423 (38.74%) / flag 1: 46338 (15.69%) / flag 2: 134589 (45.57%)
+++ FLAG_L2_FC_SCF_TEST rejected 194 values (+0.07%)      TOTALS: flag 0: 114201 (38.67%) / flag 1: 46366 (15.70%) / flag 2: 134783 (45.64%)
+++ FLAG_L2_FC_SIGNAL_STRENGTH_TEST rejected 9808 values (+3.32%)      TOTALS: flag 0: 110029 (37.25%) / flag 1: 40730 (13.79%) / flag 2: 144591 (48.96%)
+++ FLAG_L2_FC_CO2_VM97_SPIKE_HF_TEST rejected 942 values (+0.32%)      TOTALS: flag 0: 109335 (37.02%) / flag 1: 40482 (13.71%) / flag 2: 145533 (49.27%)
+++ FLAG_L2_FC_CO2_VM97_AMPLITUDE_RESOLUTION_HF_TEST rejected 3826 values (+1.30%)      TOTALS: flag 0: 106807 (36.16%) / flag 1: 39184 (13.27%) / flag 2: 149359 (50.57%)
+++ FLAG_L2_FC_CO2_VM97_DROPOUT_TEST rejected 0 values (+0.00%)      TOTALS: flag 0: 106807 (36.16%) / flag 1: 39184 (13.27%) / flag 2: 149359 (50.57%)
+++ FLAG_L2_FC_VM97_AOA_HF_TEST rejected 2607 values (+0.88%)      TOTALS: flag 0: 105860 (35.84%) / flag 1: 37524 (12.70%) / flag 2: 151966 (51.45%)
+++ FLAG_L3.2_NEE_L3.1_QCF_OUTLIER_ABSLIM_TEST rejected 2038 values (+0.69%)      TOTALS: flag 0: 105590 (35.75%) / flag 1: 35756 (12.11%) / flag 2: 154004 (52.14%)
+++ FLAG_L3.2_NEE_L3.1_QCF_OUTLIER_MANUAL_TEST rejected 731 values (+0.25%)      TOTALS: flag 0: 105303 (35.65%) / flag 1: 35312 (11.96%) / flag 2: 154735 (52.39%)
+++ FLAG_L3.2_NEE_L3.1_QCF_OUTLIER_HAMPELDTNT_TEST rejected 4302 values (+1.46%)      TOTALS: flag 0: 103478 (35.04%) / flag 1: 32835 (11.12%) / flag 2: 159037 (53.85%)
+++ FLAG_L3.2_NEE_L3.1_QCF_OUTLIER_LOCALSD_TEST rejected 282 values (+0.10%)      TOTALS: flag 0: 103432 (35.02%) / flag 1: 32599 (11.04%) / flag 2: 159319 (53.94%)
+++ FLAG_L3.3_CUT_50_NEE_L3.1_USTAR_TEST rejected 16564 values (+5.61%)      TOTALS: flag 0: 92913 (31.46%) / flag 1: 26554 (8.99%) / flag 2: 175883 (59.55%)

In total, 175883 (59.55%) of the available records were rejected in this step.
INFO Rejected DAYTIME records where QCF flag >= 2
INFO Rejected NIGHTTIME records where QCF flag >= 1
```

```
========================================
SUMMARY: FLAG_L3.3_CUT_50_NEE_L3.1_QCF, QCF FLAG FOR NEE_L3.1
========================================
Between 2005-01-01 00:15 and 2024-12-31 23:45 ...
    Total flux records BEFORE quality checks: 295350 (84.23% of potential)
    Available flux records AFTER quality checks: 119467 (40.45% of total)
    Rejected flux records: 175883 (59.55% of total)
    Potential flux records: 350640
    Potential flux records missed: 55290 (15.77% of potential)
```

## Level 4.2: NEE Partitioning (planned)

- _planned_
- Nighttime method based on Reichstein et al (2005)
- Daytime method based on Lasslop et al. (2010)
- Modified daytime method based on Keenan et al. (2019)

---
