# Used Software

## Jupyter notebooks

* **Jupyter notebooks** were used to run [diive](https://github.com/holukas/diive) code during dataset creation. 

## bico
*Prepares raw data files that are used in creating Level-0 and Level-1.*
* [bico](https://github.com/holukas/bico): Binary converter to convert original eddy covariance raw data files (irregular compressed binary files) to regular ASCII files.  Used versions `v1.6.3` and `v1.6.5`.
* [Overview of processing progress on Google Docs](https://docs.google.com/spreadsheets/d/1KXaTtckHqOGULcr9nwL0FJ-xDnMJUFeDaXX8zh0fbJo/edit?usp=sharing) (binary conversion and Level-0 and Level-1 calculations), this sheet was used during processing.

## fluxrun
*Produces Level-0 and Level-1 fluxes.*
* [fluxrun](https://github.com/holukas/fluxrun): Python wrapper for executing EddyPro. Originally developed to save the output of the EddyPro console to a text file. It also generates (simple) plots of the results. Makes it simples to execute EddyPro in parallel. Was made for internal use and is thus more tailored to needs of the Grassland Sciences group. Used version `v1.4.1`.
* [Overview of processing progress on Google Docs](https://docs.google.com/spreadsheets/d/1KXaTtckHqOGULcr9nwL0FJ-xDnMJUFeDaXX8zh0fbJo/edit?usp=sharing) (binary conversion and Level-0 and Level-1 calculations), this sheet was used during processing.

## diive
*Produces Level-2, Level-3.1, Level-3.2, Level-3.3. Also produces Level-4.1 (random forest). Applied in Jupyter notebooks.*
* [diive](https://github.com/holukas/diive): Python library for (post-)processing time series data. Used for quality control, gap-filling, merging, etc.  Used versions `v0.80+`.

## REddyProc
*Produces Level-4.1 (MDS) and Level-4.2.*
- [REddyProc](https://github.com/EarthyScience/REddyProc) was used for MDS gap-filling and NEE partitioning. Used version `X.X.X`
