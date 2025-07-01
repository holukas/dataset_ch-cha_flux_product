# Overview

The dataset was created using homogenized eddy covariance (EC) flux processing sites across all years. It combines ecosystem fluxes with meteo data and detailed management information. EC measurements at the research site [CH-CHA (Chamau)]((https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-cha/)) in Switzerland started in 2005, and at the time of writing measurements are ongoing. This documentation consists of various sections that give details about the respective variables and processing steps. In addition, we provide all flux processing settings ([EddyPro settings and metadata info](https://github.com/holukas/dataset_ch-cha_flux_product/tree/main/dataset_ch-cha_flux_product/data/EddyPro_settings)) and [Jupyter notebooks](notebooks/README) (for post-processing) that were used to create the dataset.

Below you find a short summary and important info related to the different sections in this documentation. 

## Shortest description

We processed half-hourly eddy covariance fluxes of CO2, H2O, N2O, and CH4 from 20 Hz raw data using EddyPro (v7.0.9), adhering to established community guidelines. Post-processing, including quality control and gap-filling, was performed with the Python library `diive` (Hörtnagl, 2025) and the R package `REddyProc` for NEE partitioning. Our flux calculations (Level-1) involved maximizing covariance, applying tilt correction and detrending, and precisely determining time lags, with corrections for density fluctuations, instrument filtering, and sensor separation. Fluxes underwent a multi-tiered quality control: Level-2 assessed raw data completeness, spectral correction, signal strength, and statistical screening, alongside steady-state and angle-of-attack tests. We applied storage corrections at Level-3.1 and then performed sequential outlier flagging (Level-3.2) using absolute limits, manual flags, Hampel filters, rolling z-scores, local standard deviation, and local outlier factors. Level-3.3 involved USTAR flagging to identify low turbulence periods. An overall quality control flag (QCF) combined all quality tests, leading to the removal of low-quality data and moderate-quality nighttime NEE. For gap-filling (Level-4.1), we primarily used a Random Forest approach, incorporating meteorological, management, and timestamp information, along with lagged variables. In specific cases, like N2O and CH4 fluxes during grassland restoration or periods of low data availability, we employed the MDS method. Feature selection for the Random Forest models relied on permutation importance, with feature reduction based on comparison to a random variable to ensure robust model performance across years.

## Short description

Half-hourly eddy covariance (EC) fluxes of CO2, H2O, N2O and CH4 were calculated from 20Hz raw data files using the open source software EddyPro (v7.0.9, LI-COR Biosciences, USA). Flux processing generally followed established community guidelines (Aubinet et al. 2012, Nemitz et al. 2018, Sabbatini et al., 2018). Post-processing (quality control, gap-filling) was done using the Python library diive (Hörtnagl, 2025) and the R package REddyProc (NEE partitioning; Wutzler et al., 2018).

Hörtnagl, L. (2025). diive (v0.86.0). Zenodo. https://doi.org/10.5281/zenodo.15054249

### Flux calculations (Level-1)

Biosphere-atmosphere exchange was quantified by maximizing the covariance between turbulent vertical wind speed and the turbulent gas concentrations (CO2, H2O) or dry mixing ratios (N2O, CH4). Axis rotation for tilt correction using double rotation (Wilczak et al., 2001) and block average detrending were applied. Accurate time lag determination was achieved by initially searching for the maximum covariance within a wide time window (-0.05 to +10 s) for each gas and year. For CO2 and H2O, the mode of the resultant time lag distribution defined the default lag (0.3 s), and the spread of the distribution informed the appropriate window size (typically 0.05–0.5 s). The default lag was applied when a distinct covariance peak was absent during the narrow-window search. For N2O and CH4, the most frequently observed time lag from the initial broad search was adopted as the constant lag (typically 0.6–1.75 s), with the exact value depending on the specific year and experimental setup. Density fluctuations in the open-path gas measurements were compensated (Webb et al., 1980). Raw data were tested for spikes, amplitude and drop outs (Vickers and Mahrt, 1997). Fluxes were corrected for high-pass (Moncrieff et al., 2004) and low-pass (LI-7500: Horst, 1997; QCL/LGR: Fratini et al., 2012) filtering effects. In addition, a correction for instrument separation was applied for QCL/LGR fluxes (only crosswind and vertical; Horst and Lenschow, 2009). In instances where time periods were too short for direct spectral assessment, spectral correction of the fluxes was performed using the spectral assessment file derived from the closest appropriate time period.

### Quality flag expansion (Level-2)

Fluxes were then subjected to a series of quality checks. Results for each test were stored in a separate single flag using the 0-1-2 system (unless otherwise noted), where flag=0 denotes fluxes of highest quality, 1=moderate quality, 2=low quality. 
- **Steady-state and integral turbulence characteristics test** (SSITC test, Foken and Wichura, 1996). Notably, from 1 May 2022 to 30 September 2023, moderately flagged data (flag 1) was reclassified as "low quality" (flag 2) to correct for an issue with the sonic anemometer's vertical wind measurements.
- **Gas completeness test** of 20Hz raw data files (Sabbatini et al., 2018): Applied to all fluxes, this flag, calculated in diive, checks the completeness of the raw gas concentration data. (best quality: >99% available, moderate quality: between >=97% and < 99% available, low quality: <97 % or <34,920 records available).
- **Spectral correction factor (SCF) test for out-of-range values** (Sabbatini et al., 2018): applied to all fluxes (best quality: SCF < 2, moderate quality: 2 <= SCF < 4, low quality: SCF > 4).
- **Signal strength (SS) test flag**: based on the automatic gain control from the open-path IRGA, applied to CO2 and H2O fluxes (best quality: SS <= 90%, low quality > 90%).
- **Raw data statistical screening** (Vickers and Mahrt, 1997): applied to all fluxes, checks the occurrence of spikes, drop-outs and low amplitude resolution in 20 Hz raw data.  
- **Angle-of-attack (AoA) test flag**: applied to all fluxes during specific periods: 1 Jan 2008 – 31 Dec 2009, 1 Mar – 30 Apr 2016, and 10 Dec 2021 – 23 Dec 2023. This flag addressed unrealistic wind values from the sonic anemometer's vertical wind velocity. Though not a default, it effectively removed erratic data. The standard EddyPro angle of attack settings were relaxed from $\pm30^\circ$ to $\pm35^\circ$ to balance data retention and quality, resulting in new flag variables to identify good (0) and bad (2) flux records.

### Storage correction (Level-3.1)

Storage terms, calculated from single point measurements, were added to the respective flux to quantify the ecosystem exchange and correct for conditions with low turbulence (Aubinet et al., 2001).

### Outlier flagging (Level-3.2)

Outlier tests were performed on Level-3.1 fluxes, which had already undergone an initial quality control. Specifically, individual Level-2 quality flags were combined into one overall quality control flag QCF and then _temporarily_ applied to filter Level-3.1 fluxes. This ensured that the outlier detection process only considered data that had not already been marked as low quality in Level-2. The outlier tests themselves were conducted sequentially, meaning the results of one test informed the next, as running all tests on the original, unfiltered data proved ineffective.

Generally, the following outlier tests were used:

- **Absolute limits**: flag values outside a physically plausible range (NEE: $\pm50\ \mu mol\ m^{-2}\ s^{-1}$, LE: $-50$ to $+800\ Wm^{-2}$, H: $-200$ to $+400\ Wm^{-2}$, FN2O: $-5$ to $+70\ nmol\ m^{-2}\ s^{-1}$, FCH4: $-100$ to $+1100\ nmol\ m^{-2}\ s^{-1}$). The limits were determined by analyzing typical ranges for highest-quality fluxes.
- **Manual flag**: flag specific time periods, e.g., due to known instrument failure. Applied to NEE, LE and H between 1 Dec 2008 and 1 May 2019 due to instrument failure.
- **Hampel filter**, separate for daytime and nighttime. The Hampel filter identifies anomalies in time-series data using a sliding window of adjustable size. Within each window, it compares each data point to the Median Absolute Deviation (MAD). Points exceeding the MAD by a specified multiple (adjustable) are flagged as outliers. Applied to NEE, LE and H using the settings `window_length=48*13` (corresponds to 13 days of half-hourly data), `n_sigma_dt=3.5` and `n_sigma_nt=3.5` (same n_sigma for daytime and nighttime). The test was repeated until no more outliers were flagged.
- **Rolling z-score**, identify outliers based on the rolling z-score of records. For each record, the rolling z-score is calculated from the rolling mean and rolling standard deviation, centered on the respective value. Applied to FN2O (FCH4) with the settings `n_sd=8.0` (`n_sd=7.0`) and `winsize=48*3`. The test was repeated until no more outliers were flagged.
- **Local standard deviation**, with rolling median and constant (NEE, LE, H) or rolling (FN2O, FCH4) standard deviation (SD). SD was calculated across all data and then used in combination with the rolling window. Applied to all fluxes using the following respective settings for NEE/LE/H/FN2O/FCH4: `n_sd=3.5/4.5/5.0/8.0/7.0` and `winsize=48*13` (NEE, LE, H) or `winsize=48*3` (FN2O, FCH4). The test was repeated until no more outliers were flagged.
- **Local outlier factor**, separate for daytime and nighttime. Local Outlier Factor (LOF) is an unsupervised anomaly detection method. It calculates an anomaly score based on the local density deviation of a sample compared to its k-nearest neighbors. Samples with significantly lower density than their neighbors are identified as outliers. See also the official description [here](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html). Applied to LE with the settings `n_neighbors=50` and `contamination=None`. Test was not repeated, only one iteration.

### USTAR flagging (Level-3.3)

Turbulence filtering at Level-3.3 involved flagging low turbulence periods using constant USTAR thresholds (CUT) across all years. These thresholds were derived from a recent FLUXNET analysis (2005-2023) following Pastorello et al. (2020) and were applied to NEE, FN2O, and FCH4 fluxes. They were not applied to LE or H, as advection's impact on energy fluxes differs (Pastorello et al., 2020). To provide a range of best-estimate and uncertainty-bounding flux versions, three USTAR scenarios were employed: CUT_50 ($0.069898\ ms^{-1}$), CUT_16 ($0.052945\ ms^{-1}$), and CUT_84 ($0.092841\ ms^{-1}$), corresponding to the 50th, 16th, and 84th percentiles of the FLUXNET USTAR distribution, respectively.

### Overall quality control flag (QCF)

The overall quality of each 30-minute flux data record was assessed by combining quality test results from the individual Level-2, Level-3.2 and Level-3.3 quality tests into a single overall quality control flag (QCF), calculated separately for each flux. Fluxes were categorized into three quality levels: highest quality (QCF=0) fluxes successfully passed all individual quality checks; medium quality (QCF=1) fluxes had no individual tests that outright rejected the data (test flag=2) and a maximum of two tests indicating moderate quality (test flag=1); low quality (QCF=2) fluxes were characterized by at least one individual test rejecting the record or by three or more tests marking the record as moderate quality. Low-quality flux records (QCF=2) were removed from the dataset in all cases. Moderate quality fluxes (QCF=1) were retained, with the exception of nighttime NEE where moderate quality NEE fluxes were also rejected. Resulting quality-filtered time series were used in subsequent processing steps.

### Gap-filling (Level-4.1)

##### General approach

Gap-filling for all fluxes was performed using the Random Forest (RF) class `LongTermRandomForestTS` implemented in `diive`, utilizing a sliding three-year window for annual model training. The class is based on the random forest implementation in the `scikit-learn` (v1.15)  Python library. For selecting model features, we selected variables based on their demonstrated predictive ability in previous studies. Generally, predictor variables included meteorological data, management information, timestamp information, and lagged variants. Feature selection employed permutation importance and a random variable (comprising random numbers between 0 and 1) comparison for robust feature reduction. Generally used random forest hyperparameters: `n_estimators`: 500, `random_state`: 42 (fixed for reproducibility), `min_samples_split`: 2, `min_samples_leaf`: 1; other hyperparameters used their respective default values.
##### Exceptions

**Exception (2012)**: The random forest model struggled to accurately predict `FN2O` and `FCH4` following grassland restoration between 27 February 27 2012 8:00 and 16 March 2012 18:00. Consequently, these flux values were gap-filled using the classic MDS method (Reichstein et al., 2005), which utilized incoming shortwave radiation (SWIN), soil temperature (TS), and soil water content (SWC) as predictor variables, instead of relying on the random forest predictions. This involved first removing the flux values previously imputed by the random forest model for this specific period and then applying the MDS method. This alternative gap-filling approach resulted in a more plausible representation of the flux dynamics.

**Exception (2017, 2018, 2022)**: due to low flux availability for `FN2O` and `FCH4` in 2017, 2018 and 2022, respective gap-filling models were built from all available, directly measured data (2012-2022) after quality checks and then used to gap-fill these three years. A completely new gap-filled flux version for the complete time range (2012-2022) was built. From that version, gap-filled data for the three years (2017, 2018, 2022) then replaced the data in the previously gap-filled version.
#### Model features

**NEE, LE and H**: Model features for random forest gap-filling of NEE, LE and H included shortwave incoming radiation (SWIN, at 2m height), air temperature (TA, at 2m height), vapor pressure deficit (VPD, calculated from relative humidity and TA at 2m height) and management information. Each variable was included: (1) as its measured (gap-filled) time series and (2) as time series lagged by one record, pairing each data record with the respective value of the preceding record. Additionally, PREC was included as TIMESINCE variable, counting the time (as number of records) since the last precipitation event. Management information for the two grassland parcels (PARCEL-A or PARCEL-B) was included in the form of TIMESINCE variables, which counted the number of records since the most recent occurrence of specific management events, putting each record in temporal relation to past events for the respective parcel. These events included applications of mineral fertilizer, organic fertilizer, grazing, mowing, soil cultivation, sowing, and pesticide/herbicide applications. Management TIMESINCE variables were then used in combination with wind direction to create FOOTPRINT variables. These variables linked each data record to information from either PARCEL-A or PARCEL-B variables, depending on the wind's origin at the sensors, ensuring that the source parcel of the air was accounted for. This means, depending on wind direction, the FOOTPRINT variables can contain info from PARCEL-A or PARCEL-B variables. Timestamp info was included as additional features: YEAR (integer, e.g., 2021), SEASON (integer, e.g., 2 for summer months June, July and August), MONTH (integer, e.g. 7 for July), WEEK (integer, week of year, e.g., 52), DOY (integer, day of year), HOUR (integer between 0 and 23), YEARMONTH (string, year and month, e.g. 2021-07 for July 2021), YEARDOY (string, year and day of year, e.g. 2021-034), YEARWEEK (string, year and week of year, e.g., 2021-19 for week 19 in 2021).

**FN2O, FCH4**: Model features for gap-filling FN2O and FCH4 included soil temperature (TS), soil water content (SWC), precipitation (PREC) and management information. For TS, measurements at 4, 15, and 40 cm depths were used, while SWC at 15 cm and PREC at 50 cm height were included. Each variable was included as: (1) its measured (gap-filled) time series, (2) a 3-hour preceding mean, and (3) step-lagged variants representing 3, 6, 9, and 12-hour lagged means, as described by [Feigenwinter et al. (2023)](https://www.sciencedirect.com/science/article/pii/S0048969723050143?via%3Dihub). PREC, management information and timestamp information were included like for NEE, LE and H. 

**Feature importances** were calculated as **permutation importance**: Permutation feature importance assesses feature contributions to a model’s performance. It works by randomly shuffling a feature’s values, observing the resulting performance drop.

**Feature reduction** was performed by comparing feature permutation importances to a random variable, which consisted of random numbers (floats) between 0 and 1. Features with importance below the importance of the random variable were discarded. To ensure consistency across yearly models, a feature was only removed if it was deemed unimportant in _all_ yearly models. A feature was retained if it was deemed important in at least one model.

### NEE partitioning (Level-4.2)

 We used two methods to partition NEE into GPP and RECO: the nighttime method based on Reichstein et al (2005) and the daytime method based on Lasslop et al. (2010). As a notable difference to FLUXNET datasets, partitioned fluxes were calculated from NEE gap-filled using the long-term random forest method described in [Level-4.1](L4.1) (FLUXNET uses MDS gap-filled NEE).

 
---
## Flux processing chain

We follow [Swiss FluxNet's Flux Processing Chain](https://www.swissfluxnet.ethz.ch/index.php/data/ecosystem-fluxes/flux-processing-chain/) for (post-)processing eddy covariance fluxes.

The page [Flux Processing Chain](FPC) lists background info about flux processing settings used in EddyPro and post-processing steps (quality flags, outlier removal, gap-filling) and their settings. 

We use "Levels" to describe different steps in the flux processing chain: [Level-0](L0) are preliminary fluxes used to refine processing settings, [Level-1](L1) are final flux calculations, [Level-2](L2) uses the Level-1 output to calculate additional quality flags, [Level-3.1](L3.1) calculates the storage-corrected fluxes (simple addition of storage term to flux), [Level-3.2](L3.2) creates quality flags related to outliers and [Level-3.3](L3.3) creates quality flags related to turbulence (USTAR threshold used for `NEE`, `FCH4` and `FN2O`). 

Then we assess the overall quality of each specific data record by combining quality test results from multiple individual tests into one overall **Q**uality **C**ontrol **F**lag (`QCF`). Each flux has its own `QCF`. The page [QCF](QCF) shows how this overall flag is generated. After the `QCF` was calculated, it is applied to the fluxes by removing flux records of low quality, creating quality-filtered flux versions that are used in subsequent steps.

[Level-4.1](L4.1) then uses these filtered fluxes during gap-filling, creating continuous and complete time series for each flux. [Level-4.2](L4.2) describes `NEE` partitioning using 2 different methods (nighttime method, daytime method).

## Variables

The page [Variables](Variables) lists variables that are part of the dataset. Since there are many hundreds of variables, it also gives recommendations which variables to use for which purpose. Also worth mentioning here: we have a [collection of commonly used variable abbreviations](https://www.swissfluxnet.ethz.ch/index.php/data/variables/variable-abbreviations/) (with search bar) on the Swiss FluxNet homepage. 

### Naming convention

For *meteo or auxiliary* variable names, we developed a [variable naming convention](https://www.swissfluxnet.ethz.ch/index.php/data/variables/naming-convention/) that is based on FLUXNET variable names. We use the same variable abbreviations as FLUXNET, with some exceptions (e.g. we call precipitation `PREC` instead of `P`). 

Similar to FLUXNET, we also use identifiers in the variable names that describe the horizontal and vertical position where the variable was measured, along with its replicate number. However, we use identifiers slightly differently. For example, in our case the soil water content measured in the grasslandfloor at 5 cm depth is named `SWC_GF1_0.05_1`, whereas in FLUXNET the variable name would be `SWC_1_1_1`. We decided to include the depth (or height) of a sensor in the variable name because with the FLUXNET convention (using only numbers) we would need to use a complementary list explaining all variable positions.

Following our convention it is possible to understand many variables in the dataset and their position in the field directly by simply checking its name. 

### Timestamp

The dataset uses `TIMESTAMP_MIDDLE`, which refers to the middle of the averaging period. This means that for half-hourly data typical timestamps are e.g. `2021-06-05 14:15` (with data between 14:00 and 14:30), `2021-06-05 14:45` (with data between 14:30 and 15:00).

We decided against using simply `TIMESTAMP` because it does not explain when the respective averaging interval starts or stops. It is often common to use a timestamp that gives the end of the averaging interval, without mentioning this in the description or the timestamp name. This can lead to confusion. 

For comparison: FLUXNET gives two timestamps in their dataset: `TIMESTAMP_START` and `TIMESTAMP_END`. `TIMESTAMP_START` is essentially the same as `TIMESTAMP_MIDDLE`. Using `TIMESTAMP_END` and aggregating by date, then the daily value for `2021-06-05` would include records between `2021-06-05 00:00` (these data contain the last half-hour of the previous day) and `2021-06-05 23:30` (with data between 23:00 and 23:30), i.e., the first half-hour of this day is from the previous day, and the last half-hour is missing. In essence, using `TIMESTAMP_START` and `TIMESTAMP_MIDDLE` makes aggregations easier by simply relying on the date info already given in the timestamp.

### Variants

One important aspect is that we included many variables as *variants* in the dataset. These are new variables that were calculated from existing variables.
#### `MEAN3H` variants
*Mean value over the preceding 3 hours.*

 For variables `SWC`, `TS` and `PREC` we calculated `MEAN3H` variants. The variables were included as measured, and in addition also as mean value over the preceding 3 hours ([notebook](https://holukas.github.io/dataset_ch-cha_flux_product/notebooks/30_MERGE_DATA/33.2_CalcMean3HVars_SWC_TS_PREC.html), see also description in [Feigenwinter et al., 2023a](References)). 

#### Step-lagged variants

In an additional step, we used the `MEAN3H` variants for variables `SWC`, `TS` and `PREC` to calculate *step-lagged variants* ([notebook](https://holukas.github.io/dataset_ch-cha_flux_product/notebooks/30_MERGE_DATA/33.4_CalcMean3HVarsStepLag_SWC_TS_PREC.html)): in this case, the means are lagged, however, the lag is not applied continuously (1 record, 2 records, 3 records, …) but in steps (6 records, 12, 18, 24), whereby 1 record corresponds to 30MIN. `MEAN3H-18` is the mean over the 3-hour time period ending 18 records (corresponds to 9 hours) before the respective timestamp.

This approach follows the description in [Feigenwinter et al. (2023a)](References):

> We created aggregated and lagged versions of these three variables: The running mean over 3 h before the respective timestamp (mean3h) was calculated as well as lagged running means over 3 h, which started 6, 9, and 12 h before and ended 3, 6, and 9 h before the corresponding timestamp, respectively (...).

#### `TIMESINCE` variants
*Time since last occurrence.*

`TIMESINCE` variants count the number of records since the last occurrence of an event. These variants were calculated for `PREC` and all `MGMT` (management) variables. 

Especially for the `MGMT` variables the `TIMESINCE` variants are important. By calculating `TIMESINCE` variants for all `MGMT` variables, a temporal relation of each data record to preceding management events is established. Example: `TIMESINCE_MGMT_FERT_MIN_FOOTPRINT` is the number of records since the last time mineral fertilizer was applied in the footprint. 

For example: `PREC` (precipitation) was included as the original measurement, and in addition as `TIMESINCE` variant ([notebook](https://holukas.github.io/dataset_ch-cha_flux_product/notebooks/10_METEO/17.0_AddAdditionalMeteoData_PREC_SWC_TS.html#calc-timesince-variable-for-prec)), which counted the number of records (in our case one record is 30MIN) since the last precipitation event, done for each data record. 

Measurements at the site started in 2005, but management info was available since 2001. Therefore it was possible to define the `TIMESINCE` variants also for the first year 2005. 

### Different flux versions

One goal of this dataset was to keep the different flux versions after each Level. It was therefore unavoidable to use sometimes cryptic (and long) variable names. For example, after storage correction, `FC` (CO<sub>2</sub> flux) becomes `NEE` (storage-corrected CO<sub>2</sub> flux). In this case it is easy to distinguish between the storage-corrected version and the original version. Such a distinction is not straight-forward for other fluxes, they do not have a dedicated name that would imply that they are storage-corrected. Therefore, we use the suffix `_L3.1` to indicate that the respective flux was storage-corrected (e.g. `FN2O_L3.1`). To keep naming consistent, we do this also for `NEE` as `NEE_L3.1`. 

Here is an example for `FN2O` and its name throughout the processing chain, taken from the flux processing chain notebook [here](https://holukas.github.io/dataset_ch-cha_flux_product/notebooks/50_FLUX_PROCESSING_CHAIN_QCL+LGR/51.0_FluxProcessingChain_L3.3_FN2O_QCF11.html#flux-variable-names):

- `FN2O`: original input flux from final flux calculations ([Level-1](L1))
- `FN2O_L2_QCF`: flux quality-controlled with Level-2 flags, not used in any further processing steps
- `FN2O_L3.1_QCF`: flux quality-controlled with Level-2 flags, including Level-3.1 storage correction, not used in any further processing steps
- `FN2O_L3.1_L3.2_QCF`: flux quality-controlled with Level-2 and Level-3.2 flags, including Level-3.1 storage correction), not used in any further processing steps
- `FN2O_L3.1_L3.2_QCF0`: highest-quality flux (QCF=0), quality-controlled with Level-2 and Level-3.2 flags, including Level-3.1 storage correction), not used in any further processing steps

Name of flux variables used in gap-filling and all further steps:

- `FN2O_L3.1_L3.3_CUT_16_QCF`: flux quality-controlled with Level-2 and Level-3.2 flags, and after Level-3.3 USTAR filtering (CUT_16), including Level-3.1 storage correction
- `FN2O_L3.1_L3.3_CUT_50_QCF`: flux quality-controlled with Level-2 and Level-3.2 flags, and after Level-3.3 USTAR filtering (CUT_50), including Level-3.1 storage correction
- `FN2O_L3.1_L3.3_CUT_84_QCF`: flux quality-controlled with Level-2 and Level-3.2 flags, and after Level-3.3 USTAR filtering (CUT_84), including Level-3.1 storage correction 

## Meteo data

[Meteo data](Meteo_Data) describes which variables were included and how some of them were gap-filled. [Some variables were merged](Meteo_Data#data-mering) with other datasets to generate one complete time series. Generally, included data were directly measured at the station. There are some exceptions when data from a neighboring meteo stations were used to fill gaps for e.g. `PREC` (see [Feigenwinter et al., 2023b](https://doi.org/10.1016/j.agrformet.2023.109613) for more details).

Note that there are also numerous notebooks that were used to quality-screen data from recent years ([2021-2023](https://holukas.github.io/dataset_ch-cha_flux_product/notebooks/README.html#meteo-11-meteoscreening-diive-2021-2023), [2024](https://holukas.github.io/dataset_ch-cha_flux_product/notebooks/README.html#meteo-11-meteoscreening-diive-2024)). For screening older years, no notebooks are available because data were screened with a now deprecated meteoscreening tool.

Plots of non gap-filled meteo data (2005-2024) are [shown in our database here](https://dataviews.swissfluxnet.ethz.ch/d/eeewpv2d68a9sb/15de5f4?orgId=1&from=2004-12-31T23:00:00.000Z&to=2024-12-31T23:00:00.000Z&timezone=Africa%2FTunis&var-datasource=c180d4a3-13b0-4ee5-b2ec-bcb21d46c2ea&var-dataversion1=meteoscreening_diive&var-dataversion2=meteoscreening_mst&var-measurement=$__all).

## Management data

One central question during the creation of this dataset was how can management data be combined with time series data. [Management Data](Management_Data) describes how management information was converted to a time series format. The original management info is available as XLSX file and can also be downloaded from that page. There is a [notebook](https://holukas.github.io/dataset_ch-cha_flux_product/notebooks/20_MANAGEMENT/22.0_ConvertMgmtToTimeseries.html) that shows how this conversion to a time series format was done. In addition, the dataset contains `TIMESINCE` variants that put each record in temporal relation to past management events (`TIMESINCE` variables count the number of records since the most recent respective event). The notebook shows [here](https://holukas.github.io/dataset_ch-cha_flux_product/notebooks/20_MANAGEMENT/22.0_ConvertMgmtToTimeseries.html#calculate-timesince-management-event) how this looks like for management data.

## Notebooks

All Jupyter notebooks used to create the dataset were collected here: [Notebooks overview](notebooks/README.md). They contain a lot of additional information besides the code, e.g., details about specific processing steps. If you miss some important information here in the written documentation, it is very likely that one of the notebooks has that info.

## Dataset versions

Since sometimes the dataset is updated, the page [Dataset Versions](Dataset_Versions) collects info about the different data versions. At the moment I would not expect any major changes in future versions (but you never know). Normally if there is a new version of this dataset it means that we added new variables to the data, such as soil heat flux. Or we added variants of existing variables, e.g., fluxes gap-filled with the MDS method in addition to the random forest variants. 

## Other

- [Used Software](Used_Software) lists software (including links) used in the generation of this dataset
- [Instrumentation](Instrumentation) contains information about some of the used instruments.
- [Supplementary Information](SI) dives deeper into specific aspects of the dataset.
- Sometimes not all issues can be solved perfectly. Therefore, the page [Known Issues](Issues) collects information about time periods when something noteworthy happened. Also lists the solution for the respective issue. Let's hope this list stays as empty as possible.
- [Links](Links) is a collection of external links relevant to this dataset.
- References relevant to the production of this dataset are listed in [References](References). It is possible that this list is not complete, but it should contain most of the references mentioned in the main texts. I will update this list if I found a publication I missed.



