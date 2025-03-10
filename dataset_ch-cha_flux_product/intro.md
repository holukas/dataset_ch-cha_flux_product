# CH-CHA Flux Product

produced by [Lukas Hörtnagl](https://gl.ethz.ch/people/person-detail.lukas.html)

Documentation and notebooks for the PI dataset of the **intensively managed grassland ecosystem station CH-CHA (Chamau)** . The research station CH-CHA is part of [Swiss FluxNet](https://www.swissfluxnet.ethz.ch/), operated by the [Grassland Sciences Group, ETH Zurich](https://gl.ethz.ch/). Group leader: [Prof. Nina Buchmann](https://gl.ethz.ch/people/person-detail.nina.html).

This dataset contains ecosystem fluxes measured by the eddy covariance method, meteorological data and detailed management info between 2005 and 2024. More data will be added to this dataset in the future.

## Dataset versions

### **CH-CHA FP2025.2 (2005-2024) [current version]**
- release date: 7 Mar 2025
- is currently available on demand from the Grassland Sciences group server
- **Differrences to previous version**:
	- **Flux calculations Level-1, updated fluxes for 2023**: The vertical wind component `W` showed a constant offset during some time periods. Fluxes for these time periods were re-calculated separately, taking the offset into account in the EddyPro settings. See [this table](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-cha/ec-raw-binary-format-ch-cha/#Setup_since_2005), Note (28), for the exact time periods. Other time periods during the same year were also re-calculated, but without the offset time periods.
	- **Post-processing Level-2, SSITC test**: stricter setting for *all fluxes* between `2022-05-01` and `2023-09-30`. For this test flag, data of medium quality were set to bad quality. This allowed to filter out erratic flux values due to a drift towards negative numbers observed in the vertical wind component `W`. 
	- No new data were added.

### Previous versions
- CH-CHA FP2025.1 (2005-2024) | initial release | release date: 8 Feb 2025

## Contents
- [Site info CH-CHA](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-cha/): general info about the research station
- [Meteo Data](Meteo_Data): details about used meteo data and gap-filling
- [Management Data](Management_Data): describes how management information was converted to a time series format
- [Flux Calculations](Flux_Calculations): lists background info about flux processing settings used in EddyPro
- [Flux Post-processing](Flux_Post-processing): lists post-processing steps and their settings, including generation of quality flags, outlier removal and gap-filling
- [Used Software](Used_Software): lists software (including links) used in the generation of this dataset
- [Variables](Variables): list of variables in the dataset
- [Links](Links): 
- [References](References): contains references relevant to the production of this dataset
- [Notebooks overview](notebooks/README.md): Jupyter notebooks used to create the final dataset

## Eddy covariance fluxes in this dataset

- **NEE**: Net ecosystem exchange of carbon dioxide (2005-2024)
- **LE**: Latent heat flux (2005-2024)
- **H**: Sensible heat flux (2005-2024)
- **FN2O**: Nitrous oxide flux (Jan 2012 - July 2022, with eight years of good data coverage)
- **FCH4**: Methane flux (Jan 2012 - July 2022, with eight years of good data coverage)

## Upcoming updates

- *RF = gap-filled using random forest*
- *MDS = gap-filled using marginal distrubution sampling from Reichstein et al. (2005)*
- **GPP** (RF) and **RECO** (RF) from NEE (RF) partitioning
- **GPP** (MDS) and **RECO** (MDS) from NEE (MDS) partitioning
- **ET** calculated from LE (RF)
- **ET** calculated from LE (MDS)
- more meteo variables

## Acknowledgments

We acknowledge the scientific advice by Iris Feigenwinter, Yi Wang, Lukas Hörtnagl, Lutz Merbold, Werner Eugster, Kathrin Fuchs, Matthias Zeeman, Valentin Klaus and Nina Buchmann. The technical assistance in the maintenance of the QCLAS and the eddy station by Thomas Baur, Philip Meier, Markus Staudinger, Paul Linwood, Peter Plüss, Patrick Koller, Florian Käslin is greatly acknowledged. We thank Lukas Stocker and the staff at Chamau for managing the fields around the flux station. We thank Franziska Richter and Severin Henzmann for the help with field and lab work. Annika Ackermann and Roland A. Werner are greatly acknowledged for measuring biomass C and N concentrations. We thank Regine Maier for helping with the soil sampling in 2018. We also thank Dennis Imer for his scientific and Hans-Ruedi Wettstein for organisational efforts at Chamau. Many student helpers contributed to this work with their assistance in the field and in the lab. Different projects and several doctoral students helped maintaining the site, resulting in a unique and valuable longterm time series.

### Funding

This work was funded by the European Union Horizon 2020 project Developing Sustainable Permanent Grassland Systems and Policies SUPER-G (grant number 774124), the SNF projects GrassGas (200021-105949) and M4P (40FA40_154245) as well as funds from ETH Zurich.
