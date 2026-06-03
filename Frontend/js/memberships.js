document.addEventListener("DOMContentLoaded", loadMemberships);

async function loadMemberships() {
  showLoading("memberships-table-container");
  try {
    const memberships = await getData("/memberships/");
    renderMembershipsTable(memberships);
  } catch (error) {
    console.error("Error loading memberships:", error);
    showError("memberships-table-container", "Could not load memberships.");
  }
}

function renderMembershipsTable(memberships) {
  const container = document.getElementById("memberships-table-container");

  if (!memberships || memberships.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <h5>No memberships found</h5>
        <p>Create the first membership to link a member with a plan.</p>
      </div>`;
    return;
  }

  container.innerHTML = `
    <div class="table-responsive">
      <table class="table align-middle">
        <thead>
          <tr>
            <th>ID</th>
            <th>Member ID</th>
            <th>Plan ID</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${memberships.map(m => `
            <tr>
              <td>${m.id}</td>
              <td>${m.member_id}</td>
              <td>${m.plan_id}</td>
              <td>${formatDate(m.start_date)}</td>
              <td>${formatDate(m.end_date)}</td>
              <td>${renderMembershipBadge(m.status)}</td>
            </tr>`).join("")}
        </tbody>
      </table>
    </div>`;
}

function renderMembershipBadge(status) {
  if (status === "active")    return `<span class="badge badge-soft-success">Active</span>`;
  if (status === "pending")   return `<span class="badge badge-soft-warning">Pending</span>`;
  if (status === "expired")   return `<span class="badge badge-soft-danger">Expired</span>`;
  if (status === "cancelled") return `<span class="badge badge-soft-danger">Cancelled</span>`;
  return `<span class="badge badge-soft-warning">${status}</span>`;
}

function openAddModal() {
  // Set today's date as default for start date
  const today = new Date().toISOString().split("T")[0];
  document.getElementById("membershipStartDate").value = today;
  document.getElementById("form-error").classList.add("d-none");

  const modal = new bootstrap.Modal(document.getElementById("addMembershipModal"));
  modal.show();
}

async function submitAddMembership() {
  const memberId   = document.getElementById("membershipMemberId").value;
  const planId     = document.getElementById("membershipPlanId").value;
  const startDate  = document.getElementById("membershipStartDate").value;
  const status     = document.getElementById("membershipStatus").value;
  const errorDiv   = document.getElementById("form-error");

  if (!memberId) {
    errorDiv.textContent = "Member ID is required.";
    errorDiv.classList.remove("d-none");
    return;
  }
  if (!planId) {
    errorDiv.textContent = "Plan ID is required.";
    errorDiv.classList.remove("d-none");
    return;
  }
  if (!startDate) {
    errorDiv.textContent = "Start date is required.";
    errorDiv.classList.remove("d-none");
    return;
  }

  errorDiv.classList.add("d-none");

  try {
    await postData("/memberships/", {
      member_id:  parseInt(memberId),
      plan_id:    parseInt(planId),
      start_date: startDate,
      status:     status
    });

    bootstrap.Modal.getInstance(document.getElementById("addMembershipModal")).hide();
    showSuccess("Membership created successfully!");
    loadMemberships();
  } catch (error) {
    console.error("Error saving membership:", error);
    errorDiv.textContent = "Could not save membership. Check that the Member ID and Plan ID exist.";
    errorDiv.classList.remove("d-none");
  }
}