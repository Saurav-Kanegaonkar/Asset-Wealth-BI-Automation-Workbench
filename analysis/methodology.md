# Methodology

All source data is synthetic and generated with a fixed random seed of 42. The generator models private operational structures that are common in asset and wealth management reporting work but does not represent any real financial institution.

The workflow risk score combines SLA misses, exception rate, rework rate, data quality risk, incident severity, and open stakeholder request pressure. The production issue score combines incident severity, issue age, impacted users, and related data quality failures. The automation score combines manual effort, repeatability, data readiness, downstream usage, build effort, and data quality blockers.

The result is intentionally transparent. A candidate can explain each score in an interview, change the weights, and defend why the ranked queue is suitable for BI production support and workflow automation planning.
