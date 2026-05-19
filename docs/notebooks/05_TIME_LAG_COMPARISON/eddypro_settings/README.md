# EddyPro Settings for Time Lag Comparison

This folder contains EddyPro settings (.eddypro) and metadata (.metadata) files used for the time lag comparison test using 2021 data. Results inform the final time lag settings used in the main flux processing chain.

The comparison is run for both instruments: **LGR** and **QCL**.

## Settings Variants

| Variant | Search window | Default (nominal) time lag | Method |
|---|---|---|---|
| 1 | 0–10s | No | Covariance maximization |
| 2 | 0–10s | Yes | Covariance maximization |
| 3 | 0–5s | Yes | Covariance maximization |
| 4 | 0–5s | No | Covariance maximization |
| 5 | 0–5s | Yes | PWB (Vitale et al., 2024) |

## Reference

Vitale, D., et al. (2024). A pre-whitening with block-bootstrap cross-correlation procedure
for temporal alignment of eddy covariance data. *Environmental and Ecological Statistics*,
31, 219–244. https://doi.org/10.1007/s10651-024-00615-9
