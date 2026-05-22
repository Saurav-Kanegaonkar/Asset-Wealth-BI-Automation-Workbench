const currency = new Intl.NumberFormat("en-US");

const fmtPct = (value) => `${Number(value).toFixed(1)}%`;
const fmtRate = (value) => `${(Number(value) * 100).toFixed(1)}%`;

function cellClass(value, high, medium) {
  if (value >= high) return "tag tag--high";
  if (value >= medium) return "tag tag--medium";
  return "tag";
}

function renderKpis(summary) {
  const items = [
    ["Modeled volume", currency.format(summary.total_volume), "workflow items"],
    ["SLA attainment", fmtPct(summary.sla_rate), "completed in target"],
    ["Refresh success", fmtPct(summary.refresh_success_rate), "report runs"],
    ["Open incidents", summary.open_incidents, "production queue"],
    ["Metric definitions", `${summary.certified_metric_count}/${summary.metric_count}`, "certified"],
    ["Top automation hours", summary.automation_hours_top8, "weekly hours"],
  ];

  document.querySelector("#kpis").innerHTML = items
    .map(
      ([label, value, caption]) => `
        <article class="kpi-card">
          <span>${label}</span>
          <strong>${value}</strong>
          <small>${caption}</small>
        </article>
      `
    )
    .join("");
}

function renderPriority(rows) {
  document.querySelector("#priority-table").innerHTML = rows
    .map(
      (row) => `
        <tr>
          <td>${row.rank}</td>
          <td><strong>${row.workflow}</strong><small>${row.region}</small></td>
          <td>${row.business_line}</td>
          <td>${fmtRate(row.sla_rate)}</td>
          <td>${fmtRate(row.exception_rate)}</td>
          <td><span class="${cellClass(row.risk_score, 34, 26)}">${row.risk_score}</span></td>
          <td>${row.next_action}</td>
        </tr>
      `
    )
    .join("");
}

function renderAssets(rows) {
  document.querySelector("#asset-list").innerHTML = rows
    .slice(0, 5)
    .map(
      (row) => `
        <article>
          <div>
            <strong>${row.dashboard_name}</strong>
            <span>${row.audience} / ${row.refresh_frequency}</span>
          </div>
          <b>${row.certification_status}</b>
        </article>
      `
    )
    .join("");
}

function renderRiskChart(rows) {
  const maxRisk = Math.max(...rows.map((row) => Number(row.risk_score)));
  document.querySelector("#risk-chart").innerHTML = `
    <div class="panel__heading">
      <h3>Top workflow risk</h3>
      <span>Composite score</span>
    </div>
    ${rows
      .slice(0, 6)
      .map(
        (row) => `
          <div class="bar-row">
            <span>${row.workflow}</span>
            <div><i style="width:${(Number(row.risk_score) / maxRisk) * 100}%"></i></div>
            <b>${row.risk_score}</b>
          </div>
        `
      )
      .join("")}
  `;
}

function renderIncidents(rows) {
  document.querySelector("#incident-table").innerHTML = rows
    .map(
      (row) => `
        <tr>
          <td><strong>${row.incident_id}</strong><small>${row.jira_key}</small></td>
          <td><span class="tag tag--${row.severity === "P1" ? "high" : row.severity === "P2" ? "medium" : "low"}">${row.severity}</span></td>
          <td>${row.root_cause}</td>
          <td>${row.impacted_users}</td>
          <td>${row.hours_open}</td>
          <td>${row.triage_score}</td>
          <td>${row.recommended_action}</td>
        </tr>
      `
    )
    .join("");
}

function renderQuality(rows) {
  document.querySelector("#quality-list").innerHTML = rows
    .slice(0, 8)
    .map(
      (row) => `
        <article>
          <div>
            <strong>${row.check_type}</strong>
            <span>${row.check_description}</span>
          </div>
          <span class="${row.severity === "High" ? "tag tag--high" : row.severity === "Medium" ? "tag tag--medium" : "tag"}">${fmtRate(row.pass_rate)}</span>
        </article>
      `
    )
    .join("");
}

function renderAutomation(rows) {
  document.querySelector("#automation-table").innerHTML = rows
    .map(
      (row) => `
        <tr>
          <td><strong>${row.candidate_id}</strong><small>${row.jira_key}</small></td>
          <td>${row.workflow}</td>
          <td>${row.manual_hours_week}</td>
          <td>${row.data_readiness_pct}%</td>
          <td>${row.build_effort_hours}</td>
          <td><span class="${cellClass(row.value_score, 78, 62)}">${row.value_score}</span></td>
          <td>${row.recommendation}</td>
        </tr>
      `
    )
    .join("");
}

function renderMetrics(rows) {
  document.querySelector("#metric-list").innerHTML = rows
    .map(
      (row) => `
        <article>
          <div>
            <strong>${row.metric_name}</strong>
            <span>${row.source_table} / ${row.grain}</span>
          </div>
          <b>${row.definition_status}</b>
        </article>
      `
    )
    .join("");
}

function wireTabs() {
  document.querySelectorAll(".tab").forEach((button) => {
    button.addEventListener("click", () => {
      activateView(button.dataset.view);
      history.replaceState(null, "", `#${button.dataset.view}`);
    });
  });
}

function activateView(viewName) {
  const selected = document.querySelector(`.tab[data-view="${viewName}"]`) ? viewName : "cockpit";
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.toggle("is-active", tab.dataset.view === selected);
  });
  document.querySelectorAll(".view").forEach((view) => {
    view.classList.toggle("is-active", view.id === selected);
  });
}

async function init() {
  const response = await fetch("analysis/outputs/app_payload.json");
  const data = await response.json();
  renderKpis(data.summary);
  renderPriority(data.priorityQueue);
  renderAssets(data.reportAssets);
  renderRiskChart(data.priorityQueue);
  renderIncidents(data.issueTriage);
  renderQuality(data.qualityChecks);
  renderAutomation(data.automationQueue);
  renderMetrics(data.metrics);
  wireTabs();
  activateView(window.location.hash.replace("#", "") || "cockpit");
}

init();
