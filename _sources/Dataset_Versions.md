# Dataset Versions

## Current dataset version

### **CH-CHA FP2025.3 (2005-2024) [current version]**
- This release adds additional variables to the dataset and applies a different gap-filling for N2O and CH4 fluxes during 2+ weeks after grassland restoration in 2012.
- release date: 16 May 2025
- is currently available on demand from the Grassland Sciences group server
- **Differrences to previous version FP2025.2**:
	- **Correction gap-filling Feb/Mar 2012:**
	  Random forest models were not able to predict N<sub>2</sub>O and CH<sub>4</sub> fluxes satisfactorily between 27 Feb 2012 8:00 and 16 Mar 2012 18:00. Fluxes during this time period were gap-filled using the MDS method (with SW_IN, TS and SWC as predictors) instead of random forest. 
	- **Added new flux variables from NEE partitioning** (2005-2024):
		- Partitioned fluxes were calculated from the gap-filled (random forest) NEE versions (3 USTAR scenarios: 16, 50, 84)
		-  Using nighttime method (Reichstein et al., 2005):
			- `GPP_NT_CUT_16_gfRF`, `GPP_NT_CUT_50_gfRF`, `GPP_NT_CUT_84_gfRF`
			- `RECO_NT_CUT_16_gfRF`, `RECO_NT_CUT_50_gfRF`, `RECO_NT_CUT_84_gfRF`
		- Using daytime method (Lasslop et al., 2010):
			- `GPP_DT_CUT_16_gfRF`, `GPP_DT_CUT_50_gfRF`, `GPP_DT_CUT_84_gfRF`
			- `RECO_DT_CUT_16_gfRF`, `RECO_DT_CUT_50_gfRF`, `RECO_DT_CUT_84_gfRF`
	- **Added new meteo variables** (2005-2024):
		- Soil heat flux: `G_GF1_0.03_1`, `G_GF1_0.03_2`, `G_GF1_0.05_1`, `G_GF1_0.05_2`, `G_GF4_0.02_1`, `G_GF5_0.02_1` (different depths not complete over the years, sometimes only sporadically)
		- Radiation: `SW_OUT_T1_2_1`, `LW_OUT_T1_2_1`, `NETRAD_T1_2_1`, `PPFD_OUT_T1_2_2`
- For a list of previous versions see [here](Dataset_Versions).

## Previous dataset versions

### CH-CHA FP2025.2 (2005-2024)
- release date: 7 Mar 2025 
- **Differrences to previous version FP2025.1**:
	- **Flux calculations Level-1, updated fluxes for 2023**: The vertical wind component `W` showed a constant offset during some time periods. Fluxes for these time periods were re-calculated separately, taking the offset into account in the EddyPro settings. See [this table](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-cha/ec-raw-binary-format-ch-cha/#Setup_since_2005), Note (28), for the exact time periods. Other time periods during the same year were also re-calculated, but without the offset time periods.
	- **Post-processing Level-2, SSITC test**: stricter setting for *all fluxes* between `2022-05-01` and `2023-09-30`. For this test flag, data of medium quality were set to bad quality. This allowed to filter out erratic flux values due to a drift towards negative numbers observed in the vertical wind component `W`. 
	- No new data were added.

### CH-CHA FP2025.1 (2005-2024)
- initial release
- release date: 8 Feb 2025

## Upcoming updates

- [Check Issues in the GitHub repo for upcoming updates](https://github.com/holukas/dataset_ch-cha_flux_product/issues)
