# CH-CHA Flux Product

produced by [Lukas Hörtnagl](https://gl.ethz.ch/people/person-detail.lukas.html)

Documentation and notebooks for the creation of the PI dataset of the **intensively managed grassland ecosystem station [CH-CHA (Chamau)](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-cha/)** . The site is part of [Swiss FluxNet](https://www.swissfluxnet.ethz.ch/), operated by the [Grassland Sciences Group, ETH Zurich](https://gl.ethz.ch/). Group leader: [Prof. Nina Buchmann](https://gl.ethz.ch/people/person-detail.nina.html).

The dataset comprises ecosystem fluxes measured by the eddy covariance method (CO<sub>2</sub>, H<sub>2</sub>O, H, N<sub>2</sub>O, CH<sub>4</sub>), meteorological data and detailed management info between 2005 and 2024. More data will be added to this dataset in the future.

For an overview of the dataset, see [Overview](Overview).

For an overview of recent documentation updates see [here](https://github.com/holukas/dataset_ch-cha_flux_product/commits/main/).

:::{figure-md} photo-ec1
![](images/CH-CHA_2014_ECtower_Apr2014_IMG_9304-HDR.jpg)

Photo of the CH-CHA research site in April 2014. Photo: Lukas Hörtnagl, Grassland Sciences Group, ETH Zurich
:::

## Current dataset version

### **CH-CHA FP2025.3 (2005-2024) [current version]**
- This release adds additional variables to the dataset and applies a different gap-filling for N<sub>2</sub>O and CH<sub>4</sub> fluxes during 2+ weeks after grassland restoration in 2012.
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

## Acknowledgments

We acknowledge the scientific advice by Iris Feigenwinter, Yi Wang, Lukas Hörtnagl, Lutz Merbold, Werner Eugster, Kathrin Fuchs, Matthias Zeeman, Valentin Klaus and Nina Buchmann. Special thanks to Iris Feigenwinter and Yi Wang for collecting and preparing data. The technical assistance in the maintenance of the QCLAS and the eddy station by Thomas Baur, Philip Meier, Markus Staudinger, Paul Linwood, Peter Plüss, Patrick Koller, Florian Käslin is greatly acknowledged. We thank Lukas Stocker and the staff at Chamau for managing the fields around the flux station. We thank Franziska Richter and Severin Henzmann for the help with field and lab work. Annika Ackermann and Roland A. Werner are greatly acknowledged for measuring biomass C and N concentrations. We thank Regine Maier for helping with the soil sampling in 2018. We also thank Dennis Imer for his scientific and Hans-Ruedi Wettstein for organisational efforts at Chamau. Many student helpers contributed to this work with their assistance in the field and in the lab. Different projects and several doctoral students helped maintaining the site, resulting in a unique and valuable longterm time series.

### Funding

This work was funded by the European Union Horizon 2020 project Developing Sustainable Permanent Grassland Systems and Policies SUPER-G (grant number 774124), the SNF projects GrassGas (200021-105949) and M4P (40FA40_154245) as well as funds from ETH Zurich.
