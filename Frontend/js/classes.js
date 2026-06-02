document.addEventListener("DOMContentLoaded", loadClasses);

/**
 * Carga las clases desde el backend usando la ruta corregida /shifts/
 */
async function loadClasses() {
    // Usamos el contenedor definido en classes.html
    const containerId = "classes-table-container";
    showLoading(containerId); 

    try {
        // CORRECCIÓN: Se cambia "/available-shifts/" por "/shifts/" según el router del backend
        const classes = await getData("/shifts/");
        renderClassesTable(classes);
    } catch (error) {
        console.error("Error al cargar clases:", error);
        showError("No se pudieron cargar las clases. Revisa la conexión con el servidor.");
    }
}

/**
 * Renderiza la tabla de clases con los datos del backend
 */
function renderClassesTable(classes) {
    const container = document.getElementById("classes-table-container");

    if (!classes || classes.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h5>No se encontraron clases</h5>
                <p>Crea la primera clase o turno para comenzar a gestionar el horario del gimnasio.</p>
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
                        <th>Clase</th>
                        <th>Fecha</th>
                        <th>Horario</th>
                        <th>Capacidad</th>
                        <th>Disponibles</th>
                        <th>Entrenador</th>
                        <th>Estado</th>
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

/**
 * Devuelve el badge HTML según el estado
 */
function renderStatusBadge(status) {
    const statusMap = {
        'available': '<span class="badge badge-soft-success">Disponible</span>',
        'full': '<span class="badge badge-soft-danger">Lleno</span>',
        'cancelled': '<span class="badge badge-soft-danger">Cancelado</span>'
    };
    return statusMap[status] || '<span class="badge badge-soft-warning">Programado</span>';
}

/**
 * Abre el modal de creación
 */
function openAddModal() {
    const modalElement = document.getElementById("addClassModal");
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

/**
 * Envía la nueva clase al backend
 */
async function submitAddClass() {
    const name = document.getElementById("className").value.trim();
    const date = document.getElementById("classDate").value;
    const start = document.getElementById("classStart").value;
    const end = document.getElementById("classEnd").value;
    const capacity = document.getElementById("classCapacity").value;
    const trainer = document.getElementById("classTrainer").value.trim();
    const status = document.getElementById("classStatus").value;
    const errorDiv = document.getElementById("form-error");

    // Validación básica

    if (!name || !date || !start || !end || !capacity) {
        errorDiv.textContent = "Por favor, completa todos los campos obligatorios.";
        errorDiv.classList.remove("d-none");
        return;
    }

    errorDiv.classList.add("d-none");

    const newClass = {
        name: name,
        date: date,
        start_time: start,
        end_time: end,
        capacity: parseInt(capacity),
        available_slots: parseInt(capacity),
        trainer_name: trainer,
        status: status
    };

    try {
        // CORRECCIÓN: Se usa "/shifts/" para coincidir con el backend
        await postData("/shifts/", newClass);

        // Cerrar modal y limpiar
        const modalElement = document.getElementById("addClassModal");
        const modalInstance = bootstrap.Modal.getInstance(modalElement);
        if (modalInstance) modalInstance.hide();
        
        document.getElementById("addClassForm").reset();
        
        showSuccess("¡Clase añadida con éxito!");
        loadClasses(); // Recargar la tabla
    } catch (error) {
        console.error("Error al guardar clase:", error);
        errorDiv.textContent = "No se pudo guardar la clase. Inténtalo de nuevo.";
        errorDiv.classList.remove("d-none");
    }
}