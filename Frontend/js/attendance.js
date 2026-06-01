document.addEventListener("DOMContentLoaded", loadAttendance);

const mockAttendance = [
  { id: 1, member_id: 1, reservation_id: 101, check_in: "2026-06-01T09:05:00", check_out: "2026-06-01T10:00:00" },
  { id: 2, member_id: 2, reservation_id: 102, check_in: "2026-06-01T18:02:00", check_out: null },
  { id: 3, member_id: 3, reservation_id: 103, check_in: "2026-05-31T10:00:00", check_out: "2026-05-31T11:00:00" }
];

async function loadAttendance() {
  showLoading("attendance-table-container");
  try {
    let attendance = mockAttendance;
    // Cuando el backend esté listo, reemplaza la línea de arriba por:
    // attendance = await getData("/attendances/");
    renderAttendanceTable(attendance);
  } catch (error) {
    showError("attendance-table-container", "Could not load attendance records.");
  }
}

function renderAttendanceTable(records) {
  const container = document.getElementById("attendance-table-container");

  if (!records || records.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <h5>No attendance records found</h5>
        <p>Register the first attendance to start tracking.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="table-responsive">
      <table class="table align-middle">
        <thead>
          <tr>
            <th>ID</th>
            <th>Member ID</th>
            <th>Reservation ID</th>
            <th>Check-in</th>
            <th>Check-out</th>
          </tr>
        </thead>
        <tbody>
          ${records.map(r => `
            <tr>
              <td>${r.id}</td>
              <td>${r.member_id}</td>
              <td>${r.reservation_id}</td>
              <td>${r.check_in ? formatDate(r.check_in) + " " + new Date(r.check_in).toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" }) : "-"}</td>
              <td>${r.check_out ? formatDate(r.check_out) + " " + new Date(r.check_out).toLocaleTimeString("es-ES", { hour: "2-digit", minute: "2-digit" }) : '<span class="badge badge-soft-warning">Still in</span>'}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function openAddModal() {
  const modal = new bootstrap.Modal(document.getElementById("addAttendanceModal"));
  modal.show();
}

async function submitAddAttendance() {
  const memberId = document.getElementById("attendanceMemberId").value;
  const reservationId = document.getElementById("attendanceReservationId").value;
  const errorDiv = document.getElementById("form-error");

  if (!memberId || !reservationId) {
    errorDiv.textContent = "Member ID and Reservation ID are required.";
    errorDiv.classList.remove("d-none");
    return;
  }

  errorDiv.classList.add("d-none");

  const newRecord = {
    member_id: parseInt(memberId),
    reservation_id: parseInt(reservationId),
    check_in: new Date().toISOString(),
    check_out: null
  };

  try {
    // Cuando el backend esté listo, descomenta esto:
    // await postData("/attendances/", newRecord);

    mockAttendance.push({ id: mockAttendance.length + 1, ...newRecord });

    bootstrap.Modal.getInstance(document.getElementById("addAttendanceModal")).hide();
    showSuccess("Attendance registered successfully!");
    loadAttendance();
  } catch (error) {
    errorDiv.textContent = "Could not register attendance. Try again.";
    errorDiv.classList.remove("d-none");
  }
}