# Flux Post-processing

- Post-processing follows the [Swiss Fluxnet Flux Processing Chain](https://www.swissfluxnet.ethz.ch/index.php/data/ecosystem-fluxes/flux-processing-chain/)
## Overview

```{mermaid}

    flowchart
        L1F[L1 fluxes]
        L2QCF[L2 quality flags]
        L31F[L3.1 fluxes]
        L31Ffiltered[L3.1 fluxes filtered]
        L32QCF[L3.2 quality flags]
        L33QCF[L3.3 quality flags]
        QCF[overall quality flag QCF]
        L31FfilteredQCF[L3.1 fluxes filtered with QCF]
        L41F[L4.1 gap-filled fluxes]
        L42F[L4.2 partitioned fluxes]
        
        L1F --> L2QCF
        L2QCF --> L31Ffiltered
        L1F --> L31F
        L31F --> L31Ffiltered
        L31Ffiltered --> L32QCF
        L1F --> L33QCF
        
        L2QCF --> QCF
        L32QCF --> QCF
        L33QCF --> QCF
        
        QCF -- applied to storage-corrected fluxes --> L31FfilteredQCF
        L31FfilteredQCF -- gap-filling --> L41F
        
        L41F -- partitioning (NEE) --> L42F

```

- **Level-2** creates additional quality flags that are then combined to one overall quality flag `QCF` (quality control flag)
- **Level-3.1** adds the storage term to the respective flux
- **Level-3.2** detects outliers and creates additional quality flags
- **Level-3.3** creates additional quality flags based on three different constant USTAR thresholds, previously detected by FLUXNET (Pastorello et al., 2020)
- **Level-4.1** performs gap-filling (long-term random forest)
- (planned) **Level-4.2** partitions NEE fluxes into GPP and RECO


## Level 4.2: NEE Partitioning (planned)

- _planned_
- Nighttime method based on Reichstein et al (2005)
- Daytime method based on Lasslop et al. (2010)
- Modified daytime method based on Keenan et al. (2019)

---
