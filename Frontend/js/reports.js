document.addEventListener("DOMContentLoaded", () => {
    // Set default date range: last 30 days
    const today = new Date();
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(today.getDate() - 30);

    document.getElementById("endDate").value = today.toISOString().split("T")[0];
    document.getElementById("startDate").value = thirtyDaysAgo.toISOString().split("T")[0];

    loadAllReports();
});

async function loadAllReports() {
    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;

    const params = startDate && endDate
        ? `?start_date=${startDate}&end_date=${endDate}`
        : "";

    await Promise.all([
        loadIncomeReport(params),
        loadAttendanceSummary(params),
        loadAttendanceByMember(params),
        loadAttendanceByShift(params)
    ]);
}

async function loadIncomeReport(params) {
    try {
        const data = await getData(`/reports/income${params}`);
        document.getElementById("kpi-income").textContent = formatCurrency(data.total_income);
        document.getElementById("kpi-payments").textContent = data.total_payments;
    } catch (error) {
        console.error("Error loading income report:", error);
        document.getElementById("kpi-income").textContent = "Error";
        document.getElementById("kpi-payments").textContent = "Error";
    }
}

async function loadAttendanceSummary(params) {
    try {
        const data = await getData(`/reports/attendance${params}`);
        document.getElementById("kpi-total-att").textContent = data.total_attendances;
        document.getElementById("kpi-checkins").textContent = data.total_check_ins;
        document.getElementById("kpi-checkouts").textContent = data.total_check_outs;
        document.getElementById("kpi-inside").textContent = data.current_people_inside;
    } catch (error) {
        console.error("Error loading attendance summary:", error);
        ["kpi-total-att", "kpi-checkins", "kpi-checkouts", "kpi-inside"].forEach(id => {
            document.getElementById(id).textContent = "Error";
        });
    }
}

async function loadAttendanceByMember(params) {
    showLoading("attendance-by-member-container");
    try {
        const data = await getData(`/reports/attendance/by-member${params}`);

        if (!data || data.length === 0) {
            document.getElementById("attendance-by-member-container").innerHTML = `
                <div class="empty-state"><h5>No data available</h5></div>`;
            return;
        }

        document.getElementById("attendance-by-member-container").innerHTML = `
            <div class="table-responsive">
                <table class="table align-middle">
                    <thead>
                        <tr>
                            <th>Member ID</th>
                            <th>Name</th>
                            <th>Total Attendances</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.map(r => `
                            <tr>
                                <td>${r.member_id}</td>
                                <td class="fw-semibold">${r.first_name} ${r.last_name}</td>
                                <td><span class="badge badge-soft-success">${r.total_attendances}</span></td>
                            </tr>`).join("")}
                    </tbody>
                </table>
            </div>`;
    } catch (error) {
        showError("attendance-by-member-container", "Could not load attendance by member.");
    }
}

async function loadAttendanceByShift(params) {
    showLoading("attendance-by-shift-container");
    try {
        const data = await getData(`/reports/attendance/by-shift${params}`);

        if (!data || data.length === 0) {
            document.getElementById("attendance-by-shift-container").innerHTML = `
                <div class="empty-state"><h5>No data available</h5></div>`;
            return;
        }

        document.getElementById("attendance-by-shift-container").innerHTML = `
            <div class="table-responsive">
                <table class="table align-middle">
                    <thead>
                        <tr>
                            <th>Shift ID</th>
                            <th>Date</th>
                            <th>Total Attendances</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.map(r => `
                            <tr>
                                <td>${r.shift_id}</td>
                                <td>${formatDate(r.reservation_date)}</td>
                                <td><span class="badge badge-soft-success">${r.total_attendances}</span></td>
                            </tr>`).join("")}
                    </tbody>
                </table>
            </div>`;
    } catch (error) {
        showError("attendance-by-shift-container", "Could not load attendance by shift.");
    }

const API_BASE_URL = "http://localhost:8000/api/v1";

const reportState = {
  startDate: "",
  endDate: "",
};

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("reports-filter-form");

  if (form) {
    form.addEventListener("submit", handleReportSubmit);
  }

  loadReports();
});

async function handleReportSubmit(event) {
  event.preventDefault();

  reportState.startDate = document.getElementById("start_date")?.value || "";
  reportState.endDate = document.getElementById("end_date")?.value || "";

  await loadReports();
}

async function loadReports() {
  setReportStatus("Loading reports...");

  try {
    const query = buildDateQuery();

    const [
      attendanceSummary,
      attendanceByMember,
      attendanceByReservation,
      attendanceByShift,
      incomeReport,
    ] = await Promise.all([
      fetchReport(`/reports/attendance${query}`),
      fetchReport(`/reports/attendance/by-member${query}`),
      fetchReport(`/reports/attendance/by-reservation${query}`),
      fetchReport(`/reports/attendance/by-shift${query}`),
      fetchReport(`/reports/income${query}`),
    ]);

    renderAttendanceSummary(attendanceSummary);
    renderIncomeReport(incomeReport);
    renderMemberReport(attendanceByMember);
    renderReservationReport(attendanceByReservation);
    renderShiftReport(attendanceByShift);

    setReportStatus("Reports loaded");
  } catch (error) {
    console.error(error);
    setReportStatus("Reports unavailable. Check API connection or authentication.");
  }
}

function buildDateQuery() {
  const params = new URLSearchParams();

  if (reportState.startDate) {
    params.set("start_date", reportState.startDate);
  }

  if (reportState.endDate) {
    params.set("end_date", reportState.endDate);
  }

  const query = params.toString();

  return query ? `?${query}` : "";
}

async function fetchReport(endpoint) {
  const token = localStorage.getItem("ironPulseToken");

  const headers = {};

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "GET",
    headers,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
}

function renderAttendanceSummary(report) {
  setText("total-attendances", report.total_attendances ?? "No data");
  setText("completed-attendances", report.completed_attendances ?? "No data");
  setText("open-attendances", report.open_attendances ?? "No data");
}

function renderIncomeReport(report) {
  const totalIncome = Number(report.total_income || 0);

  setText("total-income", formatCurrency(totalIncome));
  setText("completed-payments", report.completed_payments ?? "No data");
  setText("average-payment", formatCurrency(Number(report.average_payment || 0)));
}

function renderMemberReport(rows) {
  renderTableRows({
    bodyId: "member-report-body",
    emptyMessage: "No member attendance data loaded yet.",
    rows,
    columns: [
      "member_id",
      "member_name",
      "total_attendances",
    ],
  });
}

function renderReservationReport(rows) {
  renderTableRows({
    bodyId: "reservation-report-body",
    emptyMessage: "No reservation attendance data loaded yet.",
    rows,
    columns: [
      "reservation_id",
      "reservation_date",
      "total_attendances",
    ],
  });
}

function renderShiftReport(rows) {
  renderTableRows({
    bodyId: "shift-report-body",
    emptyMessage: "No shift attendance data loaded yet.",
    rows,
    columns: [
      "shift_id",
      "class_name",
      "total_attendances",
    ],
  });
}

function renderTableRows({ bodyId, emptyMessage, rows, columns }) {
  const tableBody = document.getElementById(bodyId);

  if (!tableBody) return;

  if (!Array.isArray(rows) || rows.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="${columns.length}" class="empty-table-message">
          ${emptyMessage}
        </td>
      </tr>
    `;
    return;
  }

  tableBody.innerHTML = rows
    .map((row) => {
      const cells = columns
        .map((column) => `<td>${formatValue(row[column])}</td>`)
        .join("");

      return `<tr>${cells}</tr>`;
    })
    .join("");
}

function setText(id, value) {
  const element = document.getElementById(id);

  if (!element) return;

  element.textContent = value;
}

function setReportStatus(message) {
  const element = document.getElementById("reports-status");

  if (!element) return;

  element.textContent = message;
}

function formatValue(value) {
  if (value === null || value === undefined || value === "") {
    return "-";
  }

  if (typeof value === "number") {
    return value.toLocaleString("en-US");
  }

  return value;
}

function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "EUR",
  }).format(value);
}