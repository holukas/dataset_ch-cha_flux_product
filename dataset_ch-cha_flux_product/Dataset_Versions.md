# Dataset Versions

## Current dataset version

### **CH-CHA FP2025.2 (2005-2024) [current version]**
- release date: 7 Mar 2025
- is currently available on demand from the Grassland Sciences group server
- **Differrences to previous version FP2025.1**:
	- **Flux calculations Level-1, updated fluxes for 2023**: The vertical wind component `W` showed a constant offset during some time periods. Fluxes for these time periods were re-calculated separately, taking the offset into account in the EddyPro settings. See [this table](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-cha/ec-raw-binary-format-ch-cha/#Setup_since_2005), Note (28), for the exact time periods. Other time periods during the same year were also re-calculated, but without the offset time periods.
	- **Post-processing Level-2, SSITC test**: stricter setting for *all fluxes* between `2022-05-01` and `2023-09-30`. For this test flag, data of medium quality were set to bad quality. This allowed to filter out erratic flux values due to a drift towards negative numbers observed in the vertical wind component `W`. 
	- No new data were added.

## Previous dataset versions

### CH-CHA FP2025.1 (2005-2024)
- initial release
- release date: 8 Feb 2025

## Upcoming updates

- *RF = gap-filled using random forest*
- *MDS = gap-filled using marginal distrubution sampling from Reichstein et al. (2005)*
- **GPP** (RF) and **RECO** (RF) from NEE (RF) partitioning
- **GPP** (MDS) and **RECO** (MDS) from NEE (MDS) partitioning
- **ET** calculated from LE (RF)
- **ET** calculated from LE (MDS)
- more meteo variables

