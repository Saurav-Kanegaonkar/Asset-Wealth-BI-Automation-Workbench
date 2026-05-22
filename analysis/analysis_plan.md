# Analysis Plan

## Business Question

Which client operations workflows, BI assets, and automation candidates should a data analytics analyst prioritize when supporting recurring reporting and production issue resolution?

## Method

1. Generate source-style synthetic data for workflows, report assets, refresh runs, quality checks, incidents, requests, and automation candidates.
2. Aggregate workflow-level performance across SLA attainment, exception rate, rework, data quality failures, production incidents, open requests, and manual effort.
3. Score production issues using severity, age, impacted users, and related data quality risk.
4. Score automation candidates using manual hours, repeatability, data readiness, downstream usage, effort, and quality blockers.
5. Produce ranked queues for BI operating review, production support, and sprint planning.

## Validation

The SQL file in this repo mirrors the logic an analyst would use against warehouse tables before publishing or refreshing recurring Tableau reporting.
