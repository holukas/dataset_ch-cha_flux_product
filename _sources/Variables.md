# Variables

## Eddy covariance fluxes

### Main fluxes
*Fluxes calculated from direct measurements.*

- **NEE**: Net ecosystem exchange of carbon dioxide (2005-2024)
	- 6 different versions: 3 USTAR scenarios, each with 2 different gap-filling methods (RF, MDS)
- **LE**: Latent heat flux (2005-2024)
	- 2 different versions: different gap-filling methods (RF, MDS)
- **ET**: evapotranspiration
	- 2 different versions, calculated from `LE`
- **H**: Sensible heat flux (2005-2024)
	- 2 different versions: different gap-filling methods (RF, MDS)
- **FN2O**: Nitrous oxide flux (Jan 2012 - July 2022, with eight years of good data coverage)
	- 6 different versions: 3 USTAR scenarios, each with 2 different gap-filling methods (RF, MDS)
- **FCH4**: Methane flux (Jan 2012 - July 2022, with eight years of good data coverage)
	- 6 different versions: 3 USTAR scenarios, each with 2 different gap-filling methods (RF, MDS)

### Modeled fluxes
*Fluxes calculated from main fluxes.*

- **GPP**: gross primary productivity
	- modeled from `NEE` partitioning
	- 18 different different versions, based on the 6 `NEE` versions
- **RECO**: ecosystem respiration, from `NEE` partitioning
	- modeled from `NEE` partitioning
	- 18 different different versions, based on the 6 `NEE` versions


## Meteo
*Variables in brackets are currently in progress.*

- **TA**: air temperature
- **SW_IN**: short-wave incoming radiation
- (**SW_OUT**: short-wave outgoing radiation) 
- **LW_IN**: long-wave incoming radiation
- (**LW_OUT**: long-wave outgoing radiation)
- **PA**: air pressure
- **PPFD**: photosynthetic photon flux density
- **PREC**: precipitation
- **RH**: relative humidity
- **VPD**: vapor pressure deficit, calculated from `TA` and `VPD`
- **SWC**: soil water content
- **TS**: soil temperature
- (**G**: soil heat flux)

## Auxiliary
*soon*

