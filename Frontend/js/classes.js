document.addEventListener("DOMContentLoaded", loadClasses);

async function loadClasses() {
    showLoading("classes-table-container");
    try {
        const classes = await getData("/shifts/");
        renderClassesTable(classes);
    } catch (error) {
        console.error("Error loading classes:", error);
        showError("classes-table-container", "Could not load classes. Check server connection.");
    }
}

function renderClassesTable(classes) {
    const container = document.getElementById("classes-table-container");

    if (!classes || classes.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h5>No classes found</h5>
                <p>Create the first class to start managing the gym schedule.</p>
            </div>`;
        return;
    }

    container.innerHTML = `
        <div class="table-responsive">
            <table class="table align-middle">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Class</th>
                        <th>Instructor</th>
                        <th>Day</th>
                        <th>Time</th>
                        <th>Capacity</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${classes.map(item => `
                        <tr>
                            <td>${item.id}</td>
                            <td class="fw-semibold">${item.class_name}</td>
                            <td>${item.instructor || "-"}</td>
                            <td class="text-capitalize">${item.day_of_week}</td>
                            <td>${item.start_time} - ${item.end_time}</td>
                            <td>${item.max_capacity}</td>
                            <td>${item.active_slot
                                ? '<span class="badge badge-soft-success">Active</span>'
                                : '<span class="badge badge-soft-danger">Inactive</span>'
                            }</td>
                        </tr>`).join("")}
                </tbody>
            </table>
        </div>`;
}

function openAddModal() {
    const modal = new bootstrap.Modal(document.getElementById("addClassModal"));
    modal.show();
}

async function submitAddClass() {
    const name = document.getElementById("className").value.trim();
    const instructor = document.getElementById("classInstructor").value.trim();
    const dayOfWeek = document.getElementById("classDayOfWeek").value;
    const start = document.getElementById("classStart").value;
    const end = document.getElementById("classEnd").value;
    const capacity = document.getElementById("classCapacity").value;
    const errorDiv = document.getElementById("form-error");

    if (!name || !instructor || !start || !end || !capacity) {
        errorDiv.textContent = "Please fill in all required fields.";
        errorDiv.classList.remove("d-none");
        return;
    }

    errorDiv.classList.add("d-none");

    try {
        await postData("/shifts/", {
            class_name: name,
            instructor: instructor,
            day_of_week: dayOfWeek,
            start_time: start,
            end_time: end,
            max_capacity: parseInt(capacity),
            active_slot: true
        });

        bootstrap.Modal.getInstance(document.getElementById("addClassModal")).hide();
        showSuccess("Class added successfully!");
        loadClasses();
    } catch (error) {
        console.error("Error saving class:", error);
        errorDiv.textContent = "Could not save class. Try again.";
        errorDiv.classList.remove("d-none");
    }
}