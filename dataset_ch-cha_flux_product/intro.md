# CH-CHA Flux Product
*This dataset description is currently in progress.*

produced by [Lukas Hörtnagl](https://gl.ethz.ch/people/person-detail.lukas.html)

Documentation and notebooks for the creation of the PI dataset of the **intensively managed grassland ecosystem station [CH-CHA (Chamau)](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-cha/)** . The site is part of [Swiss FluxNet](https://www.swissfluxnet.ethz.ch/), operated by the [Grassland Sciences Group, ETH Zurich](https://gl.ethz.ch/). Group leader: [Prof. Nina Buchmann](https://gl.ethz.ch/people/person-detail.nina.html).

The dataset comprises ecosystem fluxes measured by the eddy covariance method (CO<sub>2</sub>, H<sub>2</sub>O, H, N<sub>2</sub>O, CH<sub>4</sub>), meteorological data and detailed management info between 2005 and 2024. More data will be added to this dataset in the future.

For an overview of the dataset, see [here](Overview).

## Current dataset version

### **CH-CHA FP2025.2 (2005-2024) [current version]**
- release date: 7 Mar 2025
- is currently available on demand from the Grassland Sciences group server
- **Differrences to previous version FP2025.1**:
	- **Flux calculations Level-1, updated fluxes for 2023**: The vertical wind component `W` showed a constant offset during some time periods. Fluxes for these time periods were re-calculated separately, taking the offset into account in the EddyPro settings. See [this table](https://www.swissfluxnet.ethz.ch/index.php/sites/site-info-ch-cha/ec-raw-binary-format-ch-cha/#Setup_since_2005), Note (28), for the exact time periods. Other time periods during the same year were also re-calculated, but without the offset time periods.
	- **Post-processing Level-2, SSITC test**: stricter setting for *all fluxes* between `2022-05-01` and `2023-09-30`. For this test flag, data of medium quality were set to bad quality. This allowed to filter out erratic flux values due to a drift towards negative numbers observed in the vertical wind component `W`. 
	- No new data were added.
- For a list of previous versions see [here](Dataset_Versions).

## Acknowledgments

We acknowledge the scientific advice by Iris Feigenwinter, Yi Wang, Lukas Hörtnagl, Lutz Merbold, Werner Eugster, Kathrin Fuchs, Matthias Zeeman, Valentin Klaus and Nina Buchmann. The technical assistance in the maintenance of the QCLAS and the eddy station by Thomas Baur, Philip Meier, Markus Staudinger, Paul Linwood, Peter Plüss, Patrick Koller, Florian Käslin is greatly acknowledged. We thank Lukas Stocker and the staff at Chamau for managing the fields around the flux station. We thank Franziska Richter and Severin Henzmann for the help with field and lab work. Annika Ackermann and Roland A. Werner are greatly acknowledged for measuring biomass C and N concentrations. We thank Regine Maier for helping with the soil sampling in 2018. We also thank Dennis Imer for his scientific and Hans-Ruedi Wettstein for organisational efforts at Chamau. Many student helpers contributed to this work with their assistance in the field and in the lab. Different projects and several doctoral students helped maintaining the site, resulting in a unique and valuable longterm time series.

### Funding

This work was funded by the European Union Horizon 2020 project Developing Sustainable Permanent Grassland Systems and Policies SUPER-G (grant number 774124), the SNF projects GrassGas (200021-105949) and M4P (40FA40_154245) as well as funds from ETH Zurich.
