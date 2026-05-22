-- Workflow SLA, exceptions, and manual effort by business line.
select
  w.business_line,
  w.region,
  sum(d.volume) as workflow_volume,
  sum(d.sla_met) * 1.0 / nullif(sum(d.completed), 0) as sla_attainment,
  sum(d.exceptions) * 1.0 / nullif(sum(d.volume), 0) as exception_rate,
  sum(d.manual_hours) / 17.14 as weekly_manual_hours
from daily_metrics d
join workflows w
  on d.workflow_id = w.workflow_id
group by 1, 2
order by exception_rate desc;

-- Report refresh reliability by Tableau-style asset.
select
  r.asset_id,
  a.dashboard_name,
  a.certification_status,
  count(*) as refresh_runs,
  sum(case when r.status = 'Succeeded' then 1 else 0 end) * 1.0 / count(*) as refresh_success_rate,
  avg(r.duration_minutes) as avg_duration_minutes,
  max(r.source_latency_minutes) as max_source_latency_minutes
from refresh_runs r
join report_assets a
  on r.asset_id = a.asset_id
group by 1, 2, 3
having refresh_success_rate < 0.96
order by refresh_success_rate asc, max_source_latency_minutes desc;

-- Data quality controls that should block dashboard certification.
select
  q.check_id,
  q.workflow_id,
  w.workflow,
  q.check_type,
  q.pass_rate,
  q.affected_rows,
  q.severity,
  q.owner
from quality_checks q
join workflows w
  on q.workflow_id = w.workflow_id
where q.severity in ('High', 'Medium')
order by q.severity asc, q.pass_rate asc;

-- Production issue queue for daily BI support.
select
  i.incident_id,
  i.jira_key,
  i.severity,
  i.status,
  i.root_cause,
  i.impacted_users,
  i.hours_open,
  a.dashboard_name,
  w.workflow
from incidents i
join report_assets a
  on i.asset_id = a.asset_id
join workflows w
  on i.workflow_id = w.workflow_id
where i.status <> 'Resolved'
order by
  case i.severity when 'P1' then 1 when 'P2' then 2 else 3 end,
  i.hours_open desc;

-- Automation candidates ready for sprint sizing.
select
  candidate_id,
  jira_key,
  workflow,
  business_line,
  manual_hours_week,
  repeatability_pct,
  data_readiness_pct,
  build_effort_hours,
  value_score,
  recommendation
from automation_candidates
where data_readiness_pct >= 70
order by value_score desc;
