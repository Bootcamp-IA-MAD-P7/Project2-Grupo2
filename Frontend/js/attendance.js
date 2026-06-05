document.addEventListener("DOMContentLoaded", loadAttendance);

async function loadAttendance() {
    showLoading("attendance-table-container");
    try {
        const records = await getData("/attendances/");
        renderAttendanceTable(records);
    } catch (error) {
        showError("Error retrieving attendance logs.");
    }
}

function renderAttendanceTable(records) {
    const container = document.getElementById("attendance-table-container");
    container.innerHTML = `
        <table class="table">
            <thead>
                <tr>
                    <th>Member ID</th>
                    <th>Check In</th>
                    <th>Check Out</th>
                </tr>
            </thead>
            <tbody>
                ${records.map(r => `
                    <tr>
                        <td>${r.member_id}</td>
                        <td>${new Date(r.check_in).toLocaleString()}</td>
                        <td>${r.check_out ? new Date(r.check_out).toLocaleString() : 'On-site'}</td>
                    </tr>`).join("")}
            </tbody>
        </table>`;
}