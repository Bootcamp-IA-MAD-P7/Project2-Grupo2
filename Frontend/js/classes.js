document.addEventListener("DOMContentLoaded", loadClasses);

const mockClasses = [
  {
    id: 1,
    name: "Yoga Flow",
    date: "2026-06-04",
    start_time: "09:00",
    end_time: "10:00",
    capacity: 20,
    available_slots: 8,
    trainer_name: "Laura Gómez",
    status: "available"
  },
  {
    id: 2,
    name: "Functional Training",
    date: "2026-06-04",
    start_time: "18:00",
    end_time: "19:00",
    capacity: 15,
    available_slots: 0,
    trainer_name: "Carlos Ruiz",
    status: "full"
  }
];

async function loadClasses() {
  showLoading("classes-table-container");
  try {
    let classes = mockClasses;
    // Cuando el backend esté listo, reemplaza la línea de arriba por:
    // classes = await getData("/available-shifts/");
    renderClassesTable(classes);
  } catch (error) {
    showError("classes-table-container", "Could not load classes.");
  }
}

function renderClassesTable(classes) {
  const container = document.getElementById("classes-table-container");

  if (!classes || classes.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <h5>No classes found</h5>
        <p>Create the first class or shift to start managing the gym schedule.</p>
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
            <th>Class</th>
            <th>Date</th>
            <th>Time</th>
            <th>Capacity</th>
            <th>Available</th>
            <th>Trainer</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${classes.map(item => `
            <tr>
              <td>${item.id}</td>
              <td class="fw-semibold">${item.name}</td>
              <td>${formatDate(item.date)}</td>
              <td>${item.start_time} - ${item.end_time}</td>
              <td>${item.capacity}</td>
              <td>${item.available_slots}</td>
              <td>${item.trainer_name || "-"}</td>
              <td>${renderStatusBadge(item.status)}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function renderStatusBadge(status) {
  if (status === "available") return `<span class="badge badge-soft-success">Available</span>`;
  if (status === "full") return `<span class="badge badge-soft-danger">Full</span>`;
  if (status === "cancelled") return `<span class="badge badge-soft-danger">Cancelled</span>`;
  return `<span class="badge badge-soft-warning">Scheduled</span>`;
}

function openAddModal() {
  const modal = new bootstrap.Modal(document.getElementById("addClassModal"));
  modal.show();
}

async function submitAddClass() {
  const name = document.getElementById("className").value.trim();
  const date = document.getElementById("classDate").value;
  const start = document.getElementById("classStart").value;
  const end = document.getElementById("classEnd").value;
  const capacity = document.getElementById("classCapacity").value;
  const trainer = document.getElementById("classTrainer").value.trim();
  const status = document.getElementById("classStatus").value;
  const errorDiv = document.getElementById("form-error");

  if (!name || !date || !start || !end || !capacity) {
    errorDiv.textContent = "Please fill in all required fields.";
    errorDiv.classList.remove("d-none");
    return;
  }

  errorDiv.classList.add("d-none");

  const newClass = {
    name, date,
    start_time: start,
    end_time: end,
    capacity: parseInt(capacity),
    available_slots: parseInt(capacity),
    trainer_name: trainer,
    status
  };

  try {
    // Cuando el backend esté listo, descomenta esto:
    // await postData("/available-shifts/", newClass);

    // Por ahora lo añadimos al mock local
    mockClasses.push({ id: mockClasses.length + 1, ...newClass });

    bootstrap.Modal.getInstance(document.getElementById("addClassModal")).hide();
    showSuccess("Class added successfully!");
    loadClasses();
  } catch (error) {
    errorDiv.textContent = "Could not save class. Try again.";
    errorDiv.classList.remove("d-none");
  }
}