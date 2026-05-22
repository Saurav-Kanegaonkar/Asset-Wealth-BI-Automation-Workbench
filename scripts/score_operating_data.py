import csv
import json
import math
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "analysis" / "outputs"
ANALYSIS_DIR = ROOT / "analysis"
SEED = 42


random.seed(SEED)
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ANALYSIS_DIR.mkdir(exist_ok=True)


def clamp(value, low, high):
    return max(low, min(high, value))


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def pct(value):
    return round(value * 100, 1)


business_lines = [
    "Private Wealth",
    "Institutional Asset Management",
    "Alternatives Operations",
    "Managed Accounts",
    "Client Reporting",
]

regions = ["Americas", "EMEA", "APAC"]
platforms = ["Onboarding Hub", "Account Master", "Portfolio Data Mart", "Reporting Lake", "Document Vault"]
owners = ["Client Ops", "Technology", "Data Analytics", "Controls", "Reporting Enablement"]

workflow_names = [
    "New account onboarding",
    "Client reference data update",
    "Fee schedule configuration",
    "Investment guideline setup",
    "Advisor book transition",
    "Portfolio reporting entitlement",
    "Custody account mapping",
    "Alternatives subscription packet",
    "Quarterly statement preparation",
    "Tax document exception review",
    "Model portfolio rebalance approval",
    "Managed account restriction update",
    "Performance return restatement",
    "Cash movement approval",
    "Client reporting package QA",
    "Mandate closure checklist",
]


workflows = []
for index in range(1, 43):
    workflow = random.choice(workflow_names)
    business_line = random.choice(business_lines)
    region = random.choice(regions)
    criticality = random.choices(["High", "Medium", "Watch"], weights=[34, 48, 18])[0]
    complexity = round(random.uniform(0.42, 0.94), 2)
    automation_fit = round(random.uniform(0.35, 0.92), 2)
    source_count = random.randint(3, 9)
    workflows.append(
        {
            "workflow_id": f"AWM-{index:03d}",
            "workflow": workflow,
            "business_line": business_line,
            "region": region,
            "platform": random.choice(platforms),
            "owner": random.choice(owners),
            "criticality": criticality,
            "complexity_index": complexity,
            "automation_fit": automation_fit,
            "source_count": source_count,
            "tableau_asset": f"{business_line.split()[0]} {workflow.split()[0]} Control Board",
        }
    )


start_day = date(2026, 1, 5)
daily_metrics = []
for workflow in workflows:
    volume_base = random.randint(35, 210) * (1.28 if workflow["criticality"] == "High" else 1)
    for offset in range(120):
        day = start_day + timedelta(days=offset)
        weekday_factor = 0.72 if day.weekday() >= 5 else 1
        month_close_factor = 1.22 if day.day >= 25 else 1
        volume = max(4, int(random.gauss(volume_base * weekday_factor * month_close_factor, volume_base * 0.16)))
        defect_rate = clamp(random.gauss(0.021 + workflow["complexity_index"] * 0.028, 0.012), 0.004, 0.11)
        exception_rate = clamp(random.gauss(0.035 + workflow["source_count"] * 0.006, 0.018), 0.008, 0.16)
        sla_rate = clamp(random.gauss(0.963 - workflow["complexity_index"] * 0.058, 0.025), 0.78, 0.995)
        quality_rate = clamp(random.gauss(0.985 - defect_rate * 1.7, 0.012), 0.82, 0.999)
        completed = int(volume * random.uniform(0.92, 1.0))
        exceptions = int(volume * exception_rate)
        rework_items = int(volume * defect_rate)
        manual_hours = round(volume * random.uniform(0.07, 0.18) * workflow["complexity_index"], 1)
        aged_items = max(0, int(exceptions * random.uniform(0.16, 0.42) + random.gauss(2, 4)))
        freshness_minutes = int(clamp(random.gauss(52 + workflow["source_count"] * 7, 26), 8, 240))
        report_views = int(volume * random.uniform(0.35, 1.3))
        daily_metrics.append(
            {
                "date": day.isoformat(),
                "workflow_id": workflow["workflow_id"],
                "volume": volume,
                "completed": completed,
                "sla_met": int(completed * sla_rate),
                "exceptions": exceptions,
                "rework_items": rework_items,
                "aged_items": aged_items,
                "manual_hours": manual_hours,
                "quality_rate": round(quality_rate, 4),
                "data_freshness_minutes": freshness_minutes,
                "report_views": report_views,
            }
        )


report_assets = []
audiences = ["Operations leadership", "Client service", "Technology", "Risk controls", "Front office"]
certification_statuses = ["Certified", "Promoted", "Draft", "Needs owner"]
for index in range(1, 23):
    workflow = random.choice(workflows)
    status = random.choices(certification_statuses, weights=[34, 31, 23, 12])[0]
    report_assets.append(
        {
            "asset_id": f"RPT-{index:03d}",
            "dashboard_name": f"{workflow['business_line']} {workflow['workflow']} Dashboard",
            "primary_workflow_id": workflow["workflow_id"],
            "audience": random.choice(audiences),
            "owner": random.choice(owners),
            "refresh_frequency": random.choice(["Hourly", "Daily", "Twice daily", "Weekly"]),
            "certification_status": status,
            "business_criticality": workflow["criticality"],
            "avg_monthly_views": random.randint(180, 2600),
            "semantic_coverage_pct": random.randint(54, 98),
            "open_requests": random.randint(0, 9),
        }
    )


refresh_runs = []
failure_reasons = ["Source latency", "Schema drift", "Permission change", "Extract timeout", "Upstream file delay"]
for asset in report_assets:
    for offset in range(45):
        run_day = start_day + timedelta(days=75 + offset)
        failure_chance = 0.02
        if asset["certification_status"] in {"Draft", "Needs owner"}:
            failure_chance += 0.045
        if asset["refresh_frequency"] == "Hourly":
            failure_chance += 0.025
        status = "Failed" if random.random() < failure_chance else "Succeeded"
        duration = int(clamp(random.gauss(17, 8), 4, 60))
        row_count = random.randint(18_000, 1_900_000)
        refresh_runs.append(
            {
                "run_date": run_day.isoformat(),
                "asset_id": asset["asset_id"],
                "status": status,
                "duration_minutes": duration,
                "row_count": row_count,
                "source_latency_minutes": int(clamp(random.gauss(45, 36), 4, 260)),
                "failure_reason": random.choice(failure_reasons) if status == "Failed" else "",
            }
        )


quality_checks = []
check_types = [
    ("Completeness", "required field null rate"),
    ("Reconciliation", "source to report total variance"),
    ("Timeliness", "latest extract freshness"),
    ("Uniqueness", "duplicate business key rate"),
    ("Definition", "metric owner and glossary link"),
]
for workflow in workflows:
    for check_name, check_description in random.sample(check_types, 3):
        pass_rate = clamp(random.gauss(0.962 - workflow["complexity_index"] * 0.055, 0.032), 0.74, 0.999)
        affected_rows = int(max(0, random.gauss(1300 * (1 - pass_rate), 85)))
        severity = "High" if pass_rate < 0.89 or affected_rows > 190 else "Medium" if pass_rate < 0.95 else "Low"
        quality_checks.append(
            {
                "check_id": f"DQ-{len(quality_checks) + 1:03d}",
                "workflow_id": workflow["workflow_id"],
                "check_type": check_name,
                "check_description": check_description,
                "pass_rate": round(pass_rate, 4),
                "affected_rows": affected_rows,
                "severity": severity,
                "owner": random.choice(owners),
            }
        )


incidents = []
incident_roots = ["Data defect", "Refresh failure", "Metric definition gap", "Source access", "Late upstream load"]
for index in range(1, 91):
    asset = random.choice(report_assets)
    workflow = next(item for item in workflows if item["workflow_id"] == asset["primary_workflow_id"])
    severity = random.choices(["P1", "P2", "P3"], weights=[12, 41, 47])[0]
    opened = start_day + timedelta(days=random.randint(58, 118))
    status = random.choices(["Open", "In review", "Resolved"], weights=[18, 30, 52])[0]
    hours_open = random.randint(5, 96) if status != "Resolved" else random.randint(1, 48)
    impacted_users = random.randint(8, 420) * (2 if severity == "P1" else 1)
    incidents.append(
        {
            "incident_id": f"INC-{index:03d}",
            "jira_key": f"BI-{3100 + index}",
            "opened_date": opened.isoformat(),
            "severity": severity,
            "status": status,
            "root_cause": random.choice(incident_roots),
            "asset_id": asset["asset_id"],
            "workflow_id": workflow["workflow_id"],
            "impacted_users": impacted_users,
            "hours_open": hours_open,
            "owner": random.choice(owners),
        }
    )


stakeholder_requests = []
request_types = ["New metric", "Dashboard change", "Ad hoc pull", "Access request", "Definition question"]
for index in range(1, 105):
    workflow = random.choice(workflows)
    request_type = random.choice(request_types)
    stakeholder_requests.append(
        {
            "request_id": f"REQ-{index:03d}",
            "jira_key": f"OPS-{6200 + index}",
            "workflow_id": workflow["workflow_id"],
            "request_type": request_type,
            "requestor_group": random.choice(audiences),
            "priority": random.choices(["High", "Medium", "Low"], weights=[24, 50, 26])[0],
            "age_days": random.randint(1, 38),
            "status": random.choice(["Backlog", "In progress", "Waiting on owner", "Ready for release"]),
        }
    )


metric_definitions = []
metrics = [
    "SLA attainment",
    "Exception rate",
    "Aged item count",
    "Manual hours avoided",
    "Refresh success rate",
    "Data quality pass rate",
    "Production incident count",
    "Open stakeholder requests",
    "Client reporting package accuracy",
    "Rework rate",
    "Workflow cycle time",
    "Automation readiness score",
]
for index, metric in enumerate(metrics, start=1):
    certified = random.choice([True, True, True, False])
    metric_definitions.append(
        {
            "metric_id": f"MET-{index:03d}",
            "metric_name": metric,
            "business_owner": random.choice(owners),
            "tableau_measure": metric.replace(" ", "_").lower(),
            "definition_status": "Certified" if certified else random.choice(["Needs owner", "Draft"]),
            "source_table": random.choice(["daily_metrics", "refresh_runs", "quality_checks", "incidents", "automation_candidates"]),
            "grain": random.choice(["daily workflow", "report asset run", "quality check", "incident"]),
        }
    )


workflow_rollups = {}
for workflow in workflows:
    rows = [row for row in daily_metrics if row["workflow_id"] == workflow["workflow_id"]]
    incidents_for_workflow = [row for row in incidents if row["workflow_id"] == workflow["workflow_id"]]
    checks = [row for row in quality_checks if row["workflow_id"] == workflow["workflow_id"]]
    requests = [row for row in stakeholder_requests if row["workflow_id"] == workflow["workflow_id"]]
    total_volume = sum(row["volume"] for row in rows)
    total_completed = sum(row["completed"] for row in rows)
    sla_rate = sum(row["sla_met"] for row in rows) / max(1, total_completed)
    exception_rate = sum(row["exceptions"] for row in rows) / max(1, total_volume)
    rework_rate = sum(row["rework_items"] for row in rows) / max(1, total_volume)
    avg_quality = sum(row["quality_rate"] for row in rows) / len(rows)
    manual_hours = sum(row["manual_hours"] for row in rows) / 17.14
    incident_weight = sum({"P1": 9, "P2": 5, "P3": 2}[row["severity"]] for row in incidents_for_workflow)
    quality_risk = sum((1 - float(row["pass_rate"])) * 100 for row in checks)
    request_pressure = len([row for row in requests if row["status"] != "Ready for release"])
    risk_score = (
        (1 - sla_rate) * 280
        + exception_rate * 185
        + rework_rate * 150
        + quality_risk * 0.42
        + incident_weight * 1.8
        + request_pressure * 1.3
    )
    workflow_rollups[workflow["workflow_id"]] = {
        **workflow,
        "total_volume": total_volume,
        "sla_rate": sla_rate,
        "exception_rate": exception_rate,
        "rework_rate": rework_rate,
        "avg_quality": avg_quality,
        "weekly_manual_hours": manual_hours,
        "incident_count": len(incidents_for_workflow),
        "quality_check_failures": len([row for row in checks if row["severity"] in {"High", "Medium"}]),
        "open_requests": request_pressure,
        "risk_score": round(risk_score, 1),
    }


priority_queue = sorted(workflow_rollups.values(), key=lambda row: row["risk_score"], reverse=True)
priority_rows = []
for rank, row in enumerate(priority_queue, start=1):
    if row["risk_score"] >= 34:
        next_action = "Escalate source control and refresh owner"
    elif row["weekly_manual_hours"] >= 90 and row["automation_fit"] >= 0.66:
        next_action = "Move automation candidate to sprint sizing"
    elif row["quality_check_failures"] > 0:
        next_action = "Document metric definition and rerun validation"
    else:
        next_action = "Monitor in weekly operations review"
    priority_rows.append(
        {
            "rank": rank,
            "workflow_id": row["workflow_id"],
            "workflow": row["workflow"],
            "business_line": row["business_line"],
            "region": row["region"],
            "owner": row["owner"],
            "risk_score": row["risk_score"],
            "sla_rate": round(row["sla_rate"], 4),
            "exception_rate": round(row["exception_rate"], 4),
            "weekly_manual_hours": round(row["weekly_manual_hours"], 1),
            "incident_count": row["incident_count"],
            "quality_check_failures": row["quality_check_failures"],
            "open_requests": row["open_requests"],
            "next_action": next_action,
        }
    )


incident_triage = []
for incident in incidents:
    workflow = workflow_rollups[incident["workflow_id"]]
    severity_score = {"P1": 48, "P2": 28, "P3": 13}[incident["severity"]]
    age_score = min(24, incident["hours_open"] * 0.28)
    user_score = math.log(max(2, incident["impacted_users"])) * 3.7
    risk_score = round(severity_score + age_score + user_score + workflow["quality_check_failures"] * 3.5, 1)
    incident_triage.append(
        {
            **incident,
            "workflow": workflow["workflow"],
            "business_line": workflow["business_line"],
            "triage_score": risk_score,
            "recommended_action": "War room and source fix" if risk_score >= 72 else "Owner review today" if risk_score >= 52 else "Track in BI queue",
        }
    )
incident_triage = sorted(incident_triage, key=lambda row: row["triage_score"], reverse=True)


automation_candidates = []
for workflow in workflows:
    rollup = workflow_rollups[workflow["workflow_id"]]
    manual_hours = rollup["weekly_manual_hours"]
    repeatability = random.randint(54, 98)
    data_readiness = int(clamp(rollup["avg_quality"] * 100 - rollup["quality_check_failures"] * 4, 48, 99))
    downstream_users = random.randint(18, 520)
    build_effort = random.randint(32, 180)
    value_score = (
        manual_hours * 0.42
        + repeatability * 0.24
        + data_readiness * 0.22
        + math.log(downstream_users) * 6
        - build_effort * 0.11
        - rollup["quality_check_failures"] * 4
    )
    automation_candidates.append(
        {
            "candidate_id": f"AUTO-{len(automation_candidates) + 1:03d}",
            "jira_key": f"AUTO-{8100 + len(automation_candidates) + 1}",
            "workflow_id": workflow["workflow_id"],
            "workflow": workflow["workflow"],
            "business_line": workflow["business_line"],
            "manual_hours_week": round(manual_hours, 1),
            "repeatability_pct": repeatability,
            "data_readiness_pct": data_readiness,
            "downstream_users": downstream_users,
            "build_effort_hours": build_effort,
            "automation_fit": workflow["automation_fit"],
            "value_score": round(value_score, 1),
            "recommendation": "Pilot automation" if value_score >= 78 and data_readiness >= 74 else "Fix data first" if data_readiness < 70 else "Size for backlog",
        }
    )
automation_candidates = sorted(automation_candidates, key=lambda row: row["value_score"], reverse=True)


recommended_actions = []
for row in priority_rows[:16]:
    recommended_actions.append(
        {
            "action_id": f"ACT-{len(recommended_actions) + 1:03d}",
            "source": "Workflow priority queue",
            "related_id": row["workflow_id"],
            "owner": row["owner"],
            "action": row["next_action"],
            "impact": "Reduce exception exposure and improve operating review trust",
            "priority_score": row["risk_score"],
        }
    )
for row in incident_triage[:12]:
    recommended_actions.append(
        {
            "action_id": f"ACT-{len(recommended_actions) + 1:03d}",
            "source": "Production issue triage",
            "related_id": row["incident_id"],
            "owner": row["owner"],
            "action": row["recommended_action"],
            "impact": "Restore report reliability for affected stakeholders",
            "priority_score": row["triage_score"],
        }
    )
for row in automation_candidates[:12]:
    recommended_actions.append(
        {
            "action_id": f"ACT-{len(recommended_actions) + 1:03d}",
            "source": "Automation queue",
            "related_id": row["candidate_id"],
            "owner": "Data Analytics",
            "action": row["recommendation"],
            "impact": "Remove manual reporting effort and reduce recurring defects",
            "priority_score": row["value_score"],
        }
    )


refresh_success = len([row for row in refresh_runs if row["status"] == "Succeeded"]) / len(refresh_runs)
quality_pass = sum(float(row["pass_rate"]) for row in quality_checks) / len(quality_checks)
total_volume = sum(row["volume"] for row in daily_metrics)
sla_rate = sum(row["sla_met"] for row in daily_metrics) / sum(row["completed"] for row in daily_metrics)
exception_rate = sum(row["exceptions"] for row in daily_metrics) / total_volume
manual_hours_week = sum(row["manual_hours"] for row in daily_metrics) / 17.14
open_incidents = len([row for row in incidents if row["status"] != "Resolved"])
certified_metrics = len([row for row in metric_definitions if row["definition_status"] == "Certified"])
automation_hours = sum(row["manual_hours_week"] for row in automation_candidates[:8])

summary = {
    "total_volume": total_volume,
    "sla_rate": pct(sla_rate),
    "exception_rate": pct(exception_rate),
    "refresh_success_rate": pct(refresh_success),
    "quality_pass_rate": pct(quality_pass),
    "weekly_manual_hours": round(manual_hours_week, 1),
    "open_incidents": open_incidents,
    "certified_metric_count": certified_metrics,
    "metric_count": len(metric_definitions),
    "automation_hours_top8": round(automation_hours, 1),
    "top_workflow": priority_rows[0]["workflow"],
    "top_issue": incident_triage[0]["incident_id"],
    "top_automation": automation_candidates[0]["workflow"],
}


app_payload = {
    "summary": summary,
    "priorityQueue": priority_rows[:12],
    "issueTriage": incident_triage[:12],
    "automationQueue": automation_candidates[:12],
    "reportAssets": sorted(report_assets, key=lambda row: (row["certification_status"] != "Certified", -row["avg_monthly_views"]))[:10],
    "qualityChecks": sorted(quality_checks, key=lambda row: (row["severity"] != "High", row["pass_rate"]))[:10],
    "metrics": metric_definitions,
    "actions": sorted(recommended_actions, key=lambda row: row["priority_score"], reverse=True)[:18],
}


write_csv(DATA_DIR / "workflows.csv", workflows, list(workflows[0].keys()))
write_csv(DATA_DIR / "daily_metrics.csv", daily_metrics, list(daily_metrics[0].keys()))
write_csv(DATA_DIR / "report_assets.csv", report_assets, list(report_assets[0].keys()))
write_csv(DATA_DIR / "refresh_runs.csv", refresh_runs, list(refresh_runs[0].keys()))
write_csv(DATA_DIR / "quality_checks.csv", quality_checks, list(quality_checks[0].keys()))
write_csv(DATA_DIR / "incidents.csv", incidents, list(incidents[0].keys()))
write_csv(DATA_DIR / "stakeholder_requests.csv", stakeholder_requests, list(stakeholder_requests[0].keys()))
write_csv(DATA_DIR / "metric_definitions.csv", metric_definitions, list(metric_definitions[0].keys()))
write_csv(DATA_DIR / "automation_candidates.csv", automation_candidates, list(automation_candidates[0].keys()))
write_csv(DATA_DIR / "recommended_actions.csv", recommended_actions, list(recommended_actions[0].keys()))
write_csv(OUTPUT_DIR / "priority_queue.csv", priority_rows, list(priority_rows[0].keys()))
write_csv(OUTPUT_DIR / "issue_triage.csv", incident_triage, list(incident_triage[0].keys()))
write_csv(OUTPUT_DIR / "automation_queue.csv", automation_candidates, list(automation_candidates[0].keys()))

with (OUTPUT_DIR / "app_payload.json").open("w") as f:
    json.dump(app_payload, f, indent=2)


executive_findings = f"""# Executive Findings

The synthetic operating model surfaces three practical BI priorities for an asset and wealth operations reporting team.

1. The highest-risk workflow is {summary["top_workflow"]}, where SLA pressure, exceptions, quality checks, and stakeholder demand overlap.
2. Refresh reliability is {summary["refresh_success_rate"]}%, which is strong overall but still leaves production issue risk around critical Tableau assets and upstream source latency.
3. The top eight automation candidates represent {summary["automation_hours_top8"]} weekly manual hours that could be reduced after data readiness checks are completed.

Recommended operating cadence:

- Use the priority queue before weekly operations reviews to focus analyst time.
- Use the issue triage view daily when refresh failures, metric definition gaps, or data defects appear.
- Use the automation queue during sprint planning so manual reporting work is converted into Jira-sized improvements.
"""

(ANALYSIS_DIR / "executive_findings.md").write_text(executive_findings)

analysis_plan = """# Analysis Plan

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
"""

(ANALYSIS_DIR / "analysis_plan.md").write_text(analysis_plan)

methodology = f"""# Methodology

All source data is synthetic and generated with a fixed random seed of {SEED}. The generator models private operational structures that are common in asset and wealth management reporting work but does not represent any real financial institution.

The workflow risk score combines SLA misses, exception rate, rework rate, data quality risk, incident severity, and open stakeholder request pressure. The production issue score combines incident severity, issue age, impacted users, and related data quality failures. The automation score combines manual effort, repeatability, data readiness, downstream usage, build effort, and data quality blockers.

The result is intentionally transparent. A candidate can explain each score in an interview, change the weights, and defend why the ranked queue is suitable for BI production support and workflow automation planning.
"""

(ANALYSIS_DIR / "methodology.md").write_text(methodology)

measure_catalog = """# Tableau Style Measure Catalog

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
"""

(ANALYSIS_DIR / "tableau_measure_catalog.md").write_text(measure_catalog)

data_readme = """# Data

The CSV files in this folder are synthetic source-style datasets for an asset and wealth management BI operations environment.

The generator creates workflow records, daily operational metrics, Tableau-like report assets, refresh run logs, data quality checks, production incidents, stakeholder requests, metric definitions, automation candidates, and recommended actions. It uses deterministic random generation with a fixed seed so the artifact can be recreated and explained.

The data is modeled on common operational reporting structures: workflow volumes, SLA attainment, exception queues, rework, refresh reliability, source latency, schema drift, metric ownership, production incident queues, Jira-style requests, and automation sizing.
"""

(DATA_DIR / "README.md").write_text(data_readme)

print(json.dumps(summary, indent=2))
