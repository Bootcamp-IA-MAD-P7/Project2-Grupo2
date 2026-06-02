document.addEventListener("DOMContentLoaded", loadMembers);

async function loadMembers() {
    showLoading("members-table-container");
    try {
        const members = await getData("/members/");
        renderMembersTable(members);
    } catch (error) {
        console.error("Error loading members:", error);
        showError("members-table-container", "Could not load member data.");
    }
}

function renderMembersTable(members) {
    const container = document.getElementById("members-table-container");
    if (!members || members.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h5>No members found</h5>
                <p>Add the first member to get started.</p>
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
                            <td>
                                <span class="badge ${m.is_active ? 'badge-soft-success' : 'badge-soft-danger'}">
                                    ${m.is_active ? 'Active' : 'Inactive'}
                                </span>
                            </td>
                        </tr>`).join("")}
                </tbody>
            </table>
        </div>`;
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

    try {
        await postData("/members/", {
            first_name: firstName,
            last_name: lastName,
            email: email,
            phone: phone || null,
            is_active: true
        });
        bootstrap.Modal.getInstance(document.getElementById("addMemberModal")).hide();
        showSuccess("Member added successfully!");
        loadMembers();
    } catch (error) {
        errorDiv.textContent = "Could not save member. Try again.";
        errorDiv.classList.remove("d-none");
    }
}