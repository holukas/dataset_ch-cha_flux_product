# Overview

The dataset was created using homogenized eddy covariance (EC) flux processing sites across all years. It combines ecosystem fluxes with meteo data and detailed management information. EC measurements at the research site [CH-CHA (Chamau)]((https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-cha/)) in Switzerland started in 2005, and at the time of writing measurements are ongoing. This documentation consists of various sections that give details about the respective variables and processing steps. In addition, we provide all flux processing settings ([EddyPro settings and metadata info](https://github.com/holukas/dataset_ch-cha_flux_product/tree/main/dataset_ch-cha_flux_product/data/EddyPro_settings)) and [Jupyter notebooks](notebooks/README) (for post-processing) that were used to create the dataset.

Below you find a short summary and important info related to the different sections in this documentation. 

## Flux processing chain

We follow [Swiss FluxNet's Flux Processing Chain](https://www.swissfluxnet.ethz.ch/index.php/data/ecosystem-fluxes/flux-processing-chain/) for (post-)processing eddy covariance fluxes.

The page [Flux Processing Chain](FPC) lists background info about flux processing settings used in EddyPro and post-processing steps (quality flags, outlier removal, gap-filling) and their settings. 

We use "Levels" to describe different steps in the flux processing chain: [Level-0](L0) are preliminary fluxes used to refine processing settings, [Level-1](L1) are final flux calculations, [Level-2](L2) uses the Level-1 output to calculate additional quality flags, [Level-3.1](L3.1) calculates the storage-corrected fluxes (simple addition of storage term to flux), [Level-3.2](L3.2) creates quality flags related to outliers and [Level-3.3](L3.3) creates quality flags related to turbulence (USTAR threshold used for `NEE`, `FCH4` and `FN2O`). 

Then we assess the overall quality of each specific data record by combining quality test results from multiple individual tests into one overall **Q**uality **C**ontrol **F**lag (`QCF`). Each flux has its own `QCF`. The page [QCF](QCF) shows how this overall flag is generated. After the `QCF` was calculated, it is applied to the fluxes by removing flux records of low quality, creating quality-filtered flux versions that are used in subsequent steps.

[Level-4.1](L4.1) then uses these filtered fluxes during gap-filling, creating continuous and complete time series for each flux. [Level-4.2](L4.2) describes `NEE` partitioning using 3 different methods.

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



