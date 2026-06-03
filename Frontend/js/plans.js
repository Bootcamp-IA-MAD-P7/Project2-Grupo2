document.addEventListener("DOMContentLoaded", loadPlans);

async function loadPlans() {
    showLoading("plans-table-container");
    try {
        const plans = await getData("/plans/");
        renderPlansTable(plans);
    } catch (error) {
        console.error("Error loading plans:", error);
        showError("plans-table-container", "Could not load plans.");
    }
}

function renderPlansTable(plans) {
    const container = document.getElementById("plans-table-container");

    if (!plans || plans.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h5>No plans found</h5>
                <p>Add the first commercial plan to get started.</p>
            </div>`;
        return;
    }

    container.innerHTML = `
        <div class="table-responsive">
            <table class="table align-middle">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Price</th>
                        <th>Duration</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${plans.map(p => `
                        <tr>
                            <td>${p.id}</td>
                            <td class="fw-semibold">${p.name}</td>
                            <td>${p.description || "-"}</td>
                            <td>${formatCurrency(p.price)}</td>
                            <td>${p.duration_days} days</td>
                            <td>${p.active
                                ? '<span class="badge badge-soft-success">Active</span>'
                                : '<span class="badge badge-soft-danger">Inactive</span>'
                            }</td>
                        </tr>`).join("")}
                </tbody>
            </table>
        </div>`;
}

function openAddModal() {
    document.getElementById("form-error").classList.add("d-none");
    const modal = new bootstrap.Modal(document.getElementById("addPlanModal"));
    modal.show();
}

async function submitAddPlan() {
    const name        = document.getElementById("planName").value.trim();
    const description = document.getElementById("planDescription").value.trim();
    const price       = document.getElementById("planPrice").value;
    const duration    = document.getElementById("planDuration").value;
    const errorDiv    = document.getElementById("form-error");

    if (!name) {
        errorDiv.textContent = "Plan name is required.";
        errorDiv.classList.remove("d-none");
        return;
    }
    if (!price || parseFloat(price) < 0) {
        errorDiv.textContent = "Please enter a valid price.";
        errorDiv.classList.remove("d-none");
        return;
    }
    if (!duration || parseInt(duration) <= 0) {
        errorDiv.textContent = "Please enter a valid duration in days.";
        errorDiv.classList.remove("d-none");
        return;
    }

    errorDiv.classList.add("d-none");

    try {
        await postData("/plans/", {
            name:          name,
            description:   description || null,
            price:         parseFloat(price),
            duration_days: parseInt(duration),
            active:        true
        });

        bootstrap.Modal.getInstance(document.getElementById("addPlanModal")).hide();
        showSuccess("Plan added successfully!");
        loadPlans();
    } catch (error) {
        console.error("Error saving plan:", error);
        errorDiv.textContent = "Could not save plan. Try again.";
        errorDiv.classList.remove("d-none");
    }
}