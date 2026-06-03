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
    const modal = new bootstrap.Modal(document.getElementById("addPlanModal"));
    modal.show();
}

async function submitAddPlan() {
    const name = document.getElementById("planName").value.trim();
    const description = document.getElementById("planDescription").value.trim();
    const price = document.getElementById("planPrice").value;
    const duration = document.getElementById("planDuration").value;
    const errorDiv = document.getElementById("form-error");

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
            name: name,
            description: description || null,
            price: parseFloat(price),
            duration_days: parseInt(duration),
            active: true
        });

        bootstrap.Modal.getInstance(document.getElementById("addPlanModal")).hide();
        showSuccess("Plan added successfully!");
        loadPlans();
    } catch (error) {
        console.error("Error saving plan:", error);
        errorDiv.textContent = "Could not save plan. Try again.";
        errorDiv.classList.remove("d-none");
    }

const API_BASE_URL = "http://localhost:8000/api/v1";

document.addEventListener("DOMContentLoaded", () => {
  const planForm = document.querySelector('[data-api-form="/plans/"]');

  if (planForm) {
    planForm.addEventListener("submit", handleCreatePlan);
  }

  loadPlans();
});

async function loadPlans() {
  const tableBody =
    document.getElementById("plans-table-body") ||
    document.querySelector('[data-api-table^="/plans"]');

  if (!tableBody) return;

  tableBody.innerHTML = `
    <tr>
      <td colspan="5" class="empty-table-message">
        Loading plans...
      </td>
    </tr>
  `;

  try {
    const plans = await fetchData("/plans/?limit=100");
    renderPlans(plans);
  } catch (error) {
    console.error("Plans error:", error);

    tableBody.innerHTML = `
      <tr>
        <td colspan="5" class="empty-table-message">
          Plans unavailable. Check API connection or authentication.
        </td>
      </tr>
    `;
  }
}

async function handleCreatePlan(event) {
  event.preventDefault();

  const form = event.target;
  const statusMessage = form.querySelector("[data-form-status]");

  if (statusMessage) {
    statusMessage.textContent = "Saving plan...";
  }

  const payload = {
    name: form.name.value.trim(),
    price: Number(form.price.value),
    duration_days: Number(form.duration_days.value),
    description: form.description.value.trim() || null,
    active: form.active.value === "true",
  };

  try {
    await postData("/plans/", payload);

    form.reset();

    if (form.duration_days) {
      form.duration_days.value = 30;
    }

    if (form.active) {
      form.active.value = "true";
    }

    if (statusMessage) {
      statusMessage.textContent = "Plan saved successfully";
    }

    await loadPlans();
  } catch (error) {
    console.error("Create plan error:", error);

    if (statusMessage) {
      statusMessage.textContent = "Could not save plan";
    }
  }
}

async function fetchData(endpoint) {
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

async function postData(endpoint, payload) {
  const token = localStorage.getItem("ironPulseToken");

  const headers = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
}

function renderPlans(plans) {
  const tableBody =
    document.getElementById("plans-table-body") ||
    document.querySelector('[data-api-table^="/plans"]');

  if (!tableBody) return;

  if (!Array.isArray(plans) || plans.length === 0) {
    tableBody.innerHTML = `
      <tr>
        <td colspan="5" class="empty-table-message">
          No plans have been loaded yet.
        </td>
      </tr>
    `;

    return;
  }

  tableBody.innerHTML = plans
    .map((plan) => {
      return `
        <tr>
          <td>${plan.id}</td>
          <td>${plan.name}</td>
          <td>${formatCurrency(plan.price)}</td>
          <td>${plan.duration_days} days</td>
          <td>
            <span class="status-badge ${plan.active ? "" : "status-muted"}">
              ${plan.active ? "Active" : "Inactive"}
            </span>
          </td>
        </tr>
      `;
    })
    .join("");
}

function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "EUR",
  }).format(Number(value || 0));
}