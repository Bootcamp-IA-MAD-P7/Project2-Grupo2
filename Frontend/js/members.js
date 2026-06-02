document.addEventListener("DOMContentLoaded", loadMembers);

async function loadMembers() {
    showLoading("members-table-container");
    try {
        const members = await getData("/members/");
        renderMembersTable(members);
    } catch (error) {
        console.error("Error loading members:", error);
        showError("Could not load member data.");
    }
}

function renderMembersTable(members) {
    const container = document.getElementById("members-table-container");
    if (!members || members.length === 0) {
        container.innerHTML = '<div class="empty-state"><h5>No members found</h5></div>';
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
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${members.map(m => `
                        <tr>
                            <td>${m.id}</td>
                            <td>${m.first_name} ${m.last_name}</td>
                            <td>${m.email}</td>
                            <td><span class="badge ${m.is_active ? 'bg-success' : 'bg-danger'}">
                                ${m.is_active ? 'Active' : 'Inactive'}
                            </span></td>
                        </tr>`).join("")}
                </tbody>
            </table>
        </div>`;
}