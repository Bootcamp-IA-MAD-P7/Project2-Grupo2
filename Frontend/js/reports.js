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
}