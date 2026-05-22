# Tableau Style Measure Catalog

| Measure | Definition | Source |
| --- | --- | --- |
| SLA Attainment | SLA met items divided by completed items | daily_metrics |
| Exception Rate | Exceptions divided by workflow volume | daily_metrics |
| Rework Rate | Rework items divided by workflow volume | daily_metrics |
| Refresh Success Rate | Successful refresh runs divided by total refresh runs | refresh_runs |
| Data Quality Pass Rate | Average quality check pass rate | quality_checks |
| Open Production Issues | Incidents where status is not Resolved | incidents |
| Weekly Manual Hours | Daily manual hours normalized to a seven day week | daily_metrics |
| Automation Readiness | Weighted score using manual hours, repeatability, readiness, usage, and effort | automation_candidates |

These measures are written as Tableau-style semantic definitions so the portfolio shows the reporting layer and the logic behind the reporting layer.
