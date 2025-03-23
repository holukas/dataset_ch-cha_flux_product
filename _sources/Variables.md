# Variables

- [List of variable abbreviations](https://www.swissfluxnet.ethz.ch/index.php/data/variables/variable-abbreviations/): extensive list with variable names used by the Grassland Sciences group, FLUXNET, ICOS and others. Has a search bar.

## Eddy covariance fluxes

### Main fluxes
*Fluxes calculated from direct measurements.*

In addition to fluxes that were filtered according to quality 
#### NEE
- Net ecosystem exchange of carbon dioxide, `µmol CO2 m-2 s-1` (2005-2024)
- 6 different versions: 3 USTAR scenarios, each with 2 different gap-filling methods (RF, MDS)
- **Recommended variables in the dataset**:
	- `NEE_L3.1_L3.3_CUT_50_QCF`: fully quality-controlled flux, daytime: highest- and medium-quality fluxes, nighttime: only highest-quality fluxes, not gap-filled
	- `NEE_L3.1_L3.3_CUT_50_QCF_gfRF`: fully quality-controlled flux, gap-filled using long-term random forest as implemented in `diive`
	- `NEE_L3.1_L3.3_CUT_50_QCF0`: fully quality-controlled flux, but only highest-quality fluxes, not gap-filled

#### LE
- Latent heat flux, `W m-2` (2005-2024)
- 2 different versions: different gap-filling methods (RF, MDS)
- **Recommended variables in the dataset**:
	- `LE_L3.1_L3.3_CUT_NONE_QCF`: fully quality-controlled flux, daytime and nighttime: highest- and medium-quality fluxes, not gap-filled
	- `LE_L3.1_L3.3_CUT_NONE_QCF_gfRF`: fully quality-controlled flux, gap-filled using long-term random forest as implemented in `diive`
	- `LE_L3.1_L3.3_CUT_NONE_QCF0`: fully quality-controlled flux, but only highest-quality fluxes, not gap-filled

#### ET (in progress)
- Evapotranspiration, `mm h-1`
- 2 different versions, calculated from `LE`
- - **Recommended variables in the dataset**: *in progress*

#### H
- Sensible heat flux, `W m-2` (2005-2024)
- 2 different versions: different gap-filling methods (RF, MDS)
- **Recommended variables in the dataset**:
	- `H_L3.1_L3.3_CUT_NONE_QCF`: fully quality-controlled flux, daytime and nighttime: highest- and medium-quality fluxes, not gap-filled
	- `H_L3.1_L3.3_CUT_NONE_QCF_gfRF`: fully quality-controlled flux, gap-filled using long-term random forest as implemented in `diive`
	- `H_L3.1_L3.3_CUT_NONE_QCF0`: fully quality-controlled flux, but only highest-quality fluxes, not gap-filled

#### FN2O
- Nitrous oxide flux, `nmol N2O m-2 s-1` (Jan 2012 - July 2022, with eight years of good data coverage)
- 6 different versions: 3 USTAR scenarios, each with 2 different gap-filling methods (RF, MDS)
- **Recommended variables in the dataset**:
	- `FN2O_L3.1_L3.3_CUT_50_QCF`: fully quality-controlled flux, daytime and nighttime: highest- and medium-quality fluxes, not gap-filled
	- `FN2O_L3.1_L3.3_CUT_50_QCF_gfRF`: fully quality-controlled flux, gap-filled using long-term random forest as implemented in `diive`
	- `FN2O_L3.1_L3.3_CUT_50_QCF0`: fully quality-controlled flux, but only highest-quality fluxes, not gap-filled

#### FCH4
- Methane flux, `nmol CH4 m-2 s-1` (Jan 2012 - July 2022, with eight years of good data coverage)
- 6 different versions: 3 USTAR scenarios, each with 2 different gap-filling methods (RF, MDS)
- **Recommended variables in the dataset**:
	- `FCH4_L3.1_L3.3_CUT_50_QCF`: fully quality-controlled flux, daytime and nighttime: highest- and medium-quality fluxes, not gap-filled
	- `FCH4_L3.1_L3.3_CUT_50_QCF_gfRF`: fully quality-controlled flux, gap-filled using long-term random forest as implemented in `diive`
	- `FCH4_L3.1_L3.3_CUT_50_QCF0`: fully quality-controlled flux, but only highest-quality fluxes, not gap-filled

### Modeled fluxes (in progress)
*Fluxes calculated from main fluxes.*

#### GPP (in progress)
- gross primary productivity, modeled from `NEE` partitioning
- 18 different different versions, based on the 6 `NEE` versions
- **Recommended variables in the dataset**: *in progress*

#### RECO (in progress)
- ecosystem respiration, modeled from `NEE` partitioning
- 18 different different versions, based on the 6 `NEE` versions
- **Recommended variables in the dataset**: *in progress*

## Meteo
*Variables directly measured at the site.*

- **TA**: air temperature
- **SW_IN**: short-wave incoming radiation
- **SW_OUT**: short-wave outgoing radiation *in progress*
- **LW_IN**: long-wave incoming radiation
- **LW_OUT**: long-wave outgoing radiation *in progress*
- **PA**: air pressure
- **PPFD**: photosynthetic photon flux density
- **PREC**: precipitation
- **RH**: relative humidity
- **VPD**: vapor pressure deficit, calculated from `TA` and `VPD`
- **SWC**: soil water content
- **TS**: soil temperature
- **G**: soil heat flux *in progress*

## Variants
*Variants calculated from directly measured variables.*

See description in the [Overview](Overview#Variants).

## Auxiliary
*soon*

