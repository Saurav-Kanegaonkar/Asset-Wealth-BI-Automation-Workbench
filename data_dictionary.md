# Data Dictionary

| Table | Grain | Purpose |
| --- | --- | --- |
| `workflows.csv` | Client operations workflow | Business line, region, owner, platform, criticality, complexity, and automation fit metadata. |
| `daily_metrics.csv` | Workflow by day | Volume, completed items, SLA attainment, exceptions, rework, aged items, manual hours, quality rate, freshness, and report views. |
| `report_assets.csv` | BI report asset | Tableau-style dashboard inventory with audience, refresh cadence, certification status, semantic coverage, and request pressure. |
| `refresh_runs.csv` | Report asset by refresh run | Refresh status, duration, row count, source latency, and failure reason. |
| `quality_checks.csv` | Workflow quality control | Completeness, reconciliation, timeliness, uniqueness, and metric definition controls. |
| `incidents.csv` | Production support incident | Jira-style BI production issues with severity, root cause, impacted users, age, owner, and status. |
| `stakeholder_requests.csv` | Reporting request | Request type, stakeholder group, priority, age, and delivery status. |
| `metric_definitions.csv` | Semantic metric | Metric owner, Tableau-style measure name, definition status, source table, and reporting grain. |
| `automation_candidates.csv` | Workflow automation candidate | Manual hours, repeatability, data readiness, downstream users, build effort, value score, and recommendation. |
| `recommended_actions.csv` | Action item | Consolidated actions from workflow priority, production issue triage, and automation readiness scoring. |
| `analysis/outputs/priority_queue.csv` | Ranked workflow | Risk score and next action for weekly operations review. |
| `analysis/outputs/issue_triage.csv` | Ranked incident | Triage score and support action for production reporting issues. |
| `analysis/outputs/automation_queue.csv` | Ranked automation candidate | Value score and readiness recommendation for sprint planning. |
