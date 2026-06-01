document.addEventListener("DOMContentLoaded", loadMembers);

const mockMembers = [
  { id: 1, first_name: "Ana", last_name: "Martínez", email: "ana@email.com", phone: "600111222", status: "active" },
  { id: 2, first_name: "Luis", last_name: "Pérez", email: "luis@email.com", phone: "600333444", status: "active" },
  { id: 3, first_name: "María", last_name: "López", email: "maria@email.com", phone: "600555666", status: "inactive" }
];

async function loadMembers() {
  showLoading("members-table-container");
  try {
    let members = mockMembers;
    // Cuando el backend esté listo, reemplaza la línea de arriba por:
    // members = await getData("/members/");
    renderMembersTable(members);
  } catch (error) {
    showError("members-table-container", "Could not load members.");
  }
}

function renderMembersTable(members) {
  const container = document.getElementById("members-table-container");

  if (!members || members.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <h5>No members found</h5>
        <p>Add the first member to get started.</p>
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
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${members.map(m => `
            <tr>
              <td>${m.id}</td>
              <td class="fw-semibold">${m.first_name} ${m.last_name}</td>
              <td>${m.email}</td>
              <td>${m.phone || "-"}</td>
              <td>${m.status === "active"
                ? '<span class="badge badge-soft-success">Active</span>'
                : '<span class="badge badge-soft-danger">Inactive</span>'
              }</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;
}

function openAddModal() {
  const modal = new bootstrap.Modal(document.getElementById("addMemberModal"));
  modal.show();
}

async function submitAddMember() {
  const firstName = document.getElementById("memberFirstName").value.trim();
  const lastName = document.getElementById("memberLastName").value.trim();
  const email = document.getElementById("memberEmail").value.trim();
  const phone = document.getElementById("memberPhone").value.trim();
  const errorDiv = document.getElementById("form-error");

  // Validaciones
  if (!firstName || !lastName) {
    errorDiv.textContent = "First name and last name are required.";
    errorDiv.classList.remove("d-none");
    return;
  }
  if (!email || !email.includes("@")) {
    errorDiv.textContent = "Please enter a valid email address.";
    errorDiv.classList.remove("d-none");
    return;
  }

  errorDiv.classList.add("d-none");

  const newMember = { first_name: firstName, last_name: lastName, email, phone };

  try {
    // Cuando el backend esté listo, descomenta esto:
    // await postData("/members/", newMember);

    // Por ahora lo añadimos al mock local
    mockMembers.push({ id: mockMembers.length + 1, ...newMember, status: "active" });

    bootstrap.Modal.getInstance(document.getElementById("addMemberModal")).hide();
    showSuccess("Member added successfully!");
    loadMembers();
  } catch (error) {
    errorDiv.textContent = "Could not save member. Try again.";
    errorDiv.classList.remove("d-none");
  }
}